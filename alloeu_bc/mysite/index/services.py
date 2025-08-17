import requests
import datetime
import json
import logging

logger = logging.getLogger(__name__)

# Configuration de l'API Scorenco
API_URL = "https://graphql.scorenco.com/v1/graphql"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "content-type": "application/json",
    "x-hasura-role": "anonymous",
    "x-hasura-locale": "fr-FR",
    "Origin": "https://scorenco.com",
    "Referer": "https://scorenco.com/"
}
CLUB_ID = 136148
CLUB_KEYWORD = "Alloeu"

# Requête GraphQL pour récupérer les événements
QUERY_EVENTS = """
query Events($clubId: Int!, $offset: Int = 0, $limit: Int = 4, $today: date, $filter: Int!, $order: order_by!) {
  competitions_event_detail_by_club_id(
    args: {date_filter: $filter, id: $clubId},
    limit: $limit,
    offset: $offset,
    order_by: [{date: $order}, {time: $order}],
    where: {date: {_neq: $today}}
  ) {
    id
    date
    time
    status
    url
    competition { id name }
    teams
  }
}
"""

def fetch_events(filter_value, order, limit=4):
    """
    Récupère les événements depuis l'API Scorenco
    filter_value: -1 pour matchs passés, 1 pour prochains matchs
    order: 'desc' ou 'asc'
    limit: nombre maximum de résultats
    """
    today = datetime.date.today().isoformat()
    
    variables = {
        "clubId": CLUB_ID,
        "offset": 0,
        "limit": limit,
        "today": today,
        "filter": filter_value,
        "order": order
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            data=json.dumps({
                "query": QUERY_EVENTS,
                "variables": variables
            }),
            timeout=10
        )

        if response.status_code != 200:
            logger.error(f"Erreur API Scorenco ({response.status_code}): {response.text}")
            return []

        data = response.json()
        if "errors" in data:
            logger.error(f"Erreur GraphQL: {data['errors']}")
            return []

        return data["data"]["competitions_event_detail_by_club_id"]

    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur de connexion à l'API Scorenco: {e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de décodage JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        return []

def format_match_data(matches):
    """
    Formate les données des matchs pour l'affichage, y compris les logos des équipes.
    Affiche aussi les liens des logos dans la console.
    """
    formatted_matches = []
    
    for match in matches:
        try:
            is_home = False
            home_team = None
            away_team = None
            
            if len(match['teams']) >= 2:
                team1 = match['teams'][0]
                team2 = match['teams'][1]
                
                if CLUB_KEYWORD.lower() in team1['name_in_competition'].lower():
                    is_home = True
                    home_team = team1
                    away_team = team2
                elif CLUB_KEYWORD.lower() in team2['name_in_competition'].lower():
                    is_home = False
                    home_team = team2
                    away_team = team1
                else:
                    home_team = team1
                    away_team = team2

            match_date = datetime.datetime.strptime(match['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
            # Créer aussi un objet datetime pour le formatage Django
            match_date_obj = datetime.datetime.strptime(match['date'], '%Y-%m-%d').date()

            match_time = match['time'] if match['time'] else 'Heure à définir'
            # Champs calendrier
            gcal_start = None
            gcal_end = None
            if match_time != 'Heure à définir':
                try:
                    if 'T' in match_time:
                        dt = datetime.datetime.fromisoformat(match_time.replace('Z', '+00:00'))
                        dt_local = dt + datetime.timedelta(hours=2)  # Europe/Paris approx
                        hour = dt_local.hour
                        minute = dt_local.minute
                        match_time = f"{hour:02d}h{minute:02d}" if minute != 0 else f"{hour:02d}h00"
                        # Google Calendar UTC format
                        dt_utc = dt if dt.tzinfo else dt.replace(tzinfo=datetime.timezone.utc)
                        dt_utc = dt_utc.astimezone(datetime.timezone.utc)
                        gcal_start = dt_utc.strftime('%Y%m%dT%H%M%SZ')
                        gcal_end = (dt_utc + datetime.timedelta(hours=2)).strftime('%Y%m%dT%H%M%SZ')
                    elif ':' in match_time:
                        hour, minute = match_time.split(':')[:2]
                        match_time = f"{hour}h{minute}" if minute != '00' else f"{hour}h00"
                except (ValueError, IndexError):
                    pass

            # Ajout et affichage des logos
            def get_logo(team):
                if not team:
                    return None
                return team.get("logo") or team.get("logo_url") or None

            home_logo = get_logo(home_team)
            away_logo = get_logo(away_team)

            if home_team:
                home_team["logo_url"] = home_logo
            if away_team:
                away_team["logo_url"] = away_logo

            # Déterminer l'équipe du club (pour filtrage)
            club_team = None
            try:
                if home_team and (home_team.get('is_team_of_club') == 1 or (home_team.get('name_in_competition') and CLUB_KEYWORD.lower() in home_team.get('name_in_competition', '').lower())):
                    club_team = home_team
                elif away_team and (away_team.get('is_team_of_club') == 1 or (away_team.get('name_in_competition') and CLUB_KEYWORD.lower() in away_team.get('name_in_competition', '').lower())):
                    club_team = away_team
            except Exception:
                club_team = None

            club_team_id = club_team.get('team_id') if club_team else None
            club_team_name = None
            if club_team:
                club_team_name = club_team.get('name_in_club') or club_team.get('name_in_competition')

            # Titre et adresse pour calendrier
            title = None
            if home_team and away_team:
                title = f"{home_team.get('name_in_competition', 'Équipe 1')} vs {away_team.get('name_in_competition', 'Équipe 2')}"

            location_address = "Av. Henri Puchois, 62840 Laventie" if is_home else ""

            # Dates all-day pour Google Calendar si heure inconnue
            gcal_date_start = match_date_obj.strftime('%Y%m%d') if match_date_obj else None
            gcal_date_end = (match_date_obj + datetime.timedelta(days=1)).strftime('%Y%m%d') if match_date_obj else None

            # Lien externe Scorenco complet
            external_url = match.get('url', '#')
            if external_url and isinstance(external_url, str) and external_url.startswith('/'):
                external_url = f"https://scorenco.com{external_url}"

            formatted_match = {
                'id': match['id'],
                'date': match_date,
                'date_obj': match_date_obj,  # Objet date pour le formatage Django
                'time': match_time,
                'competition': f"{home_team.get('name_in_club', 'Équipe 1') if away_team else 'Équipe 1'} vs {away_team.get('name_in_club', 'Équipe 2') if away_team else 'Équipe 2'}",
                'status': match['status'],
                'is_home': is_home,
                'location': "🏠 Domicile" if is_home else "🚌 Extérieur",
                'home_team': home_team,
                'away_team': away_team,
                'url': match.get('url', '#'),
                # Métadonnées pour filtrage par équipe du club
                'club_team_id': club_team_id,
                'club_team_name': club_team_name,
                # Données calendrier
                'gcal_start': gcal_start,
                'gcal_end': gcal_end,
                'gcal_date_start': gcal_date_start,
                'gcal_date_end': gcal_date_end,
                'title': title,
                'location_address': location_address,
                'external_url': external_url,
                'has_time': gcal_start is not None,
            }

            formatted_matches.append(formatted_match)
        
        except (KeyError, IndexError, ValueError) as e:
            logger.warning(f"Erreur lors du formatage du match {match.get('id', 'inconnu')}: {e}")
            continue
    
    return formatted_matches


def get_next_matches(limit=4):
    """Récupère les prochains matchs"""
    matches = fetch_events(filter_value=1, order="asc", limit=limit)
    return format_match_data(matches)

def get_last_results(limit=4):
    """Récupère les derniers résultats"""
    matches = fetch_events(filter_value=-1, order="desc", limit=limit)
    return format_match_data(matches)
