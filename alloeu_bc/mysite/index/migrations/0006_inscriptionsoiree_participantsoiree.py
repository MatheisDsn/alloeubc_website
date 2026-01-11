# Generated migration for InscriptionSoiree and ParticipantSoiree models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_equipes_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='InscriptionSoiree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom')),
                ('prenom', models.CharField(max_length=100, verbose_name='Prénom')),
                ('email', models.EmailField(max_length=254, verbose_name='Adresse email')),
                ('telephone', models.CharField(max_length=20, verbose_name='Numéro de téléphone')),
                ('nombre_personnes', models.PositiveIntegerField(verbose_name='Nombre de personnes')),
                ('statut', models.CharField(
                    choices=[('en_attente', 'En attente'), ('valide', 'Validé'), ('refuse', 'Refusé')],
                    default='en_attente',
                    max_length=20,
                    verbose_name='Statut'
                )),
                ('date_inscription', models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")),
                ('date_validation', models.DateTimeField(blank=True, null=True, verbose_name='Date de validation')),
            ],
            options={
                'verbose_name': 'Inscription soirée festive',
                'verbose_name_plural': 'Inscriptions soirée festive',
                'ordering': ['-date_inscription'],
            },
        ),
        migrations.CreateModel(
            name='ParticipantSoiree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lien_club', models.CharField(
                    help_text='Ex: Joueur, Parent, Entraîneur, Bénévole, etc.',
                    max_length=200,
                    verbose_name='Lien avec le club'
                )),
                ('inscription', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='participants',
                    to='index.inscriptionsoiree',
                    verbose_name='Inscription'
                )),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
            },
        ),
    ]
