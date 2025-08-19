from django.core.management.base import BaseCommand
from django.utils import timezone
from news.models import Category, Article


class Command(BaseCommand):
    help = 'Crée des données d\'exemple pour les actualités'

    def handle(self, *args, **options):
        self.stdout.write('Création des données d\'exemple pour les actualités...')

        # Création des catégories
        categories_data = [
            {'name': 'Match', 'color': 'blue', 'description': 'Résultats et annonces de matchs'},
            {'name': 'Équipe', 'color': 'green', 'description': 'Actualités des équipes'},
            {'name': 'Club', 'color': 'purple', 'description': 'Actualités générales du club'},
            {'name': 'Événement', 'color': 'red', 'description': 'Événements et manifestations'},
            {'name': 'Formation', 'color': 'yellow', 'description': 'École de basket et formation'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'color': cat_data['color'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Catégorie créée: {category.name}')

        # Création des articles d'exemple
        articles_data = [
            {
                'title': 'Victoire éclatante contre l\'équipe de Lens !',
                'category': 'Match',
                'excerpt': 'Nos seniors masculins ont remporté une victoire éclatante 78-65 contre l\'équipe de Lens lors du match de samedi dernier. Une performance collective remarquable !',
                'content': '''
                Une soirée mémorable au gymnase ! Nos seniors masculins ont livré une prestation de haute volée face à l'équipe de Lens.

                Dès le premier quart-temps, nos joueurs ont imposé leur rythme avec une défense agressive et des contre-attaques rapides. Le score à la mi-temps était déjà en notre faveur : 42-28.

                Les moments forts du match :
                - Une série de 12 points consécutifs en début de 2e quart-temps
                - 15 rebonds offensifs qui ont fait la différence
                - Une adresse à 3 points exceptionnelle (8/12)
                - La performance individuelle de notre capitaine avec 22 points

                L'entraîneur était très satisfait : "L'équipe a montré un visage très séduisant. La cohésion et l'investissement défensif ont payé. C'est le fruit du travail à l'entraînement."

                Prochaine échéance : déplacement à Arras le samedi 15 février à 20h30.

                Bravo à toute l'équipe pour cette belle victoire !
                ''',
                'featured': True,
                'status': 'published'
            },
            {
                'title': 'Nouvelle recrue : Bienvenue à Antoine Martin !',
                'category': 'Équipe',
                'excerpt': 'Le club est fier d\'accueillir Antoine Martin, nouveau joueur de 24 ans en provenance du club de Douai. Un renfort de taille pour nos ambitions cette saison !',
                'content': '''
                Le club d'Alloeu Basket Club a le plaisir d'annoncer l'arrivée d'Antoine Martin dans ses rangs !

                Profil du joueur :
                - Âge : 24 ans
                - Poste : Arrière/Ailier
                - Taille : 1m88
                - Expérience : 6 années en Régionale 1

                Antoine nous arrive du club de Douai où il évoluait depuis 3 saisons. Ses statistiques parlent pour lui : 18,5 points de moyenne la saison passée avec 45% d'adresse à 3 points.

                "Je suis très heureux de rejoindre l'Alloeu BC. L'accueil a été formidable et j'ai hâte de contribuer aux objectifs du club cette saison", nous confie Antoine.

                L'entraîneur principal ajoute : "Antoine apporte l'expérience et les qualités athlétiques qui nous manquaient. Son profil polyvalent va enrichir notre collectif."

                Antoine sera présenté officiellement au public lors du prochain match à domicile. Souhaitons-lui la bienvenue dans la famille d'Alloeu BC !
                ''',
                'featured': False,
                'status': 'published'
            },
            {
                'title': 'Stage de basket pendant les vacances de février',
                'category': 'Formation',
                'excerpt': 'Un stage de 3 jours est organisé pour les jeunes de 8 à 16 ans pendant les vacances de février. Inscriptions ouvertes !',
                'content': '''
                L'école de basket d'Alloeu organise un stage exceptionnel pendant les vacances de février !

                Informations pratiques :
                - Dates : du mardi 18 au jeudi 20 février 2025
                - Horaires : 9h30 - 16h30 (avec pause repas)
                - Lieu : Gymnase municipal d'Alloeu
                - Public : jeunes de 8 à 16 ans (tous niveaux)
                - Tarif : 60€ pour les 3 jours (repas inclus)

                Programme du stage :
                - Fondamentaux techniques (dribble, tir, passe)
                - Situations de jeu 2c2 et 3c3
                - Perfectionnement tactique
                - Tournois et matchs
                - Activités ludiques

                L'encadrement sera assuré par nos éducateurs diplômés d'État et d'anciens joueurs professionnels.

                Inscriptions :
                - En ligne sur notre site web
                - Au gymnase les mardis et jeudis de 18h à 20h
                - Par téléphone au 03.21.XX.XX.XX

                Attention, places limitées à 24 participants ! Les inscriptions se font par ordre d'arrivée.

                N'hésitez pas à nous contacter pour plus d'informations.
                ''',
                'featured': False,
                'status': 'published'
            },
            {
                'title': 'Assemblée générale annuelle - Vendredi 8 mars',
                'category': 'Club',
                'excerpt': 'L\'assemblée générale annuelle du club se déroulera le vendredi 8 mars à 19h30 en salle de réunion. Tous les adhérents sont invités.',
                'content': '''
                Tous les membres et adhérents de l'Alloeu Basket Club sont cordialement invités à participer à l'assemblée générale annuelle.

                Informations pratiques :
                - Date : Vendredi 8 mars 2025
                - Heure : 19h30
                - Lieu : Salle de réunion de la mairie d'Alloeu
                - Durée prévue : 2h

                Ordre du jour :
                1. Rapport moral du président
                2. Rapport financier du trésorier
                3. Bilan sportif de la saison
                4. Présentation des projets 2025-2026
                5. Élection du nouveau bureau
                6. Questions diverses

                Cette assemblée est l'occasion de :
                - Faire le bilan de l'année écoulée
                - Présenter les orientations futures
                - Échanger avec les dirigeants
                - Proposer des idées et projets

                La présence de chacun est importante pour la vie démocratique de notre association. Votre participation contribue aux décisions qui concernent l'avenir du club.

                Un pot de l'amitié clôturera cette soirée, permettant de poursuivre les échanges dans une ambiance conviviale.

                Merci de confirmer votre présence avant le 5 mars.
                ''',
                'featured': False,
                'status': 'published'
            },
            {
                'title': 'Tournoi jeunes : nos équipes brillent !',
                'category': 'Match',
                'excerpt': 'Excellent week-end pour nos équipes jeunes lors du tournoi régional. Nos U15 terminent 2e et nos U13 remportent leur catégorie !',
                'content': '''
                Week-end de compétition exceptionnel pour les équipes jeunes de l'Alloeu BC lors du tournoi régional de Béthune !

                Résultats de nos équipes :

                U13 - CHAMPIONS ! 🏆
                - 1er de leur poule avec 4 victoires
                - Finale remportée 45-42 contre Arras
                - Mention spéciale à Lucas (meilleur marqueur du tournoi)

                U15 - Vice-champions ! 🥈
                - Parcours sans faute jusqu'en finale
                - Défaite honorable 52-48 contre Douai
                - Belle progression collective visible

                U17 - 4e place
                - Deux victoires, une défaite en poule
                - Défaite en petite finale mais bon état d'esprit

                Les entraîneurs soulignent l'excellent comportement de tous nos jeunes, leur fair-play et leur détermination.

                Ce tournoi confirme la qualité du travail mené à l'école de basket. Les résultats sportifs récompensent l'investissement des joueurs et de l'encadrement.

                Félicitations à tous nos champions et futurs champions !

                Prochaine échéance : championnat départemental le week-end prochain.
                ''',
                'featured': True,
                'status': 'published'
            },
        ]

        for article_data in articles_data:
            category = Category.objects.get(name=article_data['category'])
            
            article, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'category': category,
                    'excerpt': article_data['excerpt'],
                    'content': article_data['content'],
                    'featured': article_data['featured'],
                    'status': article_data['status'],
                    'published_at': timezone.now()
                }
            )
            
            if created:
                self.stdout.write(f'Article créé: {article.title}')

        self.stdout.write(
            self.style.SUCCESS('Données d\'exemple créées avec succès !')
        )
