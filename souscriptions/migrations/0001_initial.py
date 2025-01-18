# Generated by Django 5.1.4 on 2025-01-11 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeSouscripteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code')),
                ('nom', models.CharField(choices=[('Personne Physique', 'Personne Physique'), ('Personne Morale', 'Personne Morale')], max_length=100, verbose_name='Nom')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')),
            ],
            options={
                'verbose_name': 'Type de Souscripteur',
                'verbose_name_plural': 'Types de Souscripteurs',
            },
        ),
        migrations.CreateModel(
            name='SouscriptionEffectuee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_transaction', models.CharField(max_length=50, unique=True, verbose_name='Numéro de Transaction')),
                ('date_souscription', models.DateTimeField(auto_now_add=True, verbose_name='Date de Souscription')),
                ('nom_complet', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nom Complet')),
                ('date_naissance', models.DateField(blank=True, null=True, verbose_name='Date de Naissance')),
                ('lieu_naissance', models.CharField(blank=True, max_length=100, null=True, verbose_name='Lieu de Naissance')),
                ('profession', models.CharField(blank=True, max_length=100, null=True, verbose_name='Profession')),
                ('genre', models.CharField(blank=True, max_length=10, null=True, verbose_name='Genre')),
                ('document', models.CharField(blank=True, max_length=20, null=True, verbose_name='Type de Document')),
                ('numero_piece', models.CharField(blank=True, max_length=50, null=True, verbose_name='Numéro de Pièce')),
                ('date_expiration', models.DateField(blank=True, null=True, verbose_name="Date d'Expiration")),
                ('lieu_etablissement', models.CharField(blank=True, max_length=100, null=True, verbose_name="Lieu d'Établissement")),
                ('date_etablissement', models.DateField(blank=True, null=True, verbose_name="Date d'Établissement")),
                ('raison_sociale', models.CharField(blank=True, max_length=200, null=True, verbose_name='Raison Sociale')),
                ('forme_juridique', models.CharField(blank=True, max_length=20, null=True, verbose_name='Forme Juridique')),
                ('rccm', models.CharField(blank=True, max_length=50, null=True, verbose_name='RCCM')),
                ('ifu', models.CharField(blank=True, max_length=50, null=True, verbose_name='IFU')),
                ('siege_social', models.CharField(blank=True, max_length=200, null=True, verbose_name='Siège Social')),
                ('nom_representant', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nom du Représentant')),
                ('prenom_representant', models.CharField(blank=True, max_length=100, null=True, verbose_name='Prénom du Représentant')),
                ('fonction_representant', models.CharField(blank=True, max_length=100, null=True, verbose_name='Fonction du Représentant')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('pays', models.CharField(max_length=100, verbose_name='Pays')),
                ('region', models.CharField(max_length=100, verbose_name='Région')),
                ('ville', models.CharField(max_length=100, verbose_name='Ville')),
                ('adresse', models.TextField(verbose_name='Adresse')),
                ('surface', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Surface')),
                ('cout_unitaire', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Coût Unitaire')),
                ('prix_total', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Prix Total')),
                ('acompte', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Acompte')),
                ('reste_a_payer', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Reste à Payer')),
                ('section', models.CharField(max_length=100, verbose_name='Section')),
                ('lot', models.CharField(max_length=100, verbose_name='Lot')),
                ('montant_souscription', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='Frais de Souscription')),
                ('methode_paiement', models.CharField(max_length=50, verbose_name='Méthode de Paiement')),
                ('date_paiement', models.DateTimeField(auto_now_add=True, verbose_name='Date de Paiement')),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operations.operations', verbose_name='Opération')),
                ('parcelle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operations.listesparcelles', verbose_name='Parcelle')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operations.positionparcelle', verbose_name='Position')),
                ('type_parcelle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='operations.typeparcelle', verbose_name='Type de Parcelle')),
                ('type_souscripteur', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='souscriptions.typesouscripteur', verbose_name='Type de Souscripteur')),
            ],
            options={
                'verbose_name': 'Souscription Effectuée',
                'verbose_name_plural': 'Souscriptions Effectuées',
                'ordering': ['-date_souscription'],
            },
        ),
        migrations.CreateModel(
            name='SouscripteurPhysique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_complet', models.CharField(max_length=150, verbose_name='Nom Complet')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('date_naissance', models.DateField(verbose_name='Date de Naissance')),
                ('lieu_naissance', models.CharField(max_length=100, verbose_name='Lieu de Naissance')),
                ('profession', models.CharField(max_length=100, verbose_name='Profession')),
                ('genre', models.CharField(choices=[('Homme', 'Homme'), ('Femme', 'Femme')], max_length=10, verbose_name='Genre')),
                ('document', models.CharField(choices=[('CIN', "Carte Nationale d'Identité Burkinabé"), ('PASSEPORT', 'Passeport'), ('PERMIS_SEJOUR', 'Permis de Séjour'), ('CARTE_RESIDENT', 'Carte de Résident')], max_length=20, verbose_name='Type de Document')),
                ('numero_piece', models.CharField(max_length=50, verbose_name='Numéro de Pièce')),
                ('date_expiration', models.DateField(verbose_name="Date d'Expiration")),
                ('lieu_etablissement', models.CharField(max_length=100, verbose_name="Lieu d'Établissement")),
                ('date_etablissement', models.DateField(verbose_name="Date d'Établissement")),
                ('pays', models.CharField(choices=[('Burkina Faso', 'Burkina Faso'), ("Côte d'Ivoire", "Côte d'Ivoire"), ('Sénégal', 'Sénégal'), ('Mali', 'Mali'), ('Niger', 'Niger'), ('Togo', 'Togo'), ('Bénin', 'Bénin'), ('Guinée', 'Guinée'), ('Ghana', 'Ghana'), ('Nigéria', 'Nigéria'), ('Algérie', 'Algérie'), ('Afrique du Sud', 'Afrique du Sud'), ('Congo (RDC)', 'Congo (RDC)'), ('Kenya', 'Kenya'), ('Maroc', 'Maroc'), ('Tunisie', 'Tunisie'), ('Égypte', 'Égypte'), ('Tanzanie', 'Tanzanie'), ('Zambie', 'Zambie'), ('Ouganda', 'Ouganda')], max_length=100, verbose_name='Pays')),
                ('region', models.CharField(max_length=100, verbose_name='Région')),
                ('ville', models.CharField(max_length=100, verbose_name='Ville')),
                ('adresse', models.TextField(verbose_name='Adresse')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')),
                ('type_souscripteur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='souscriptions.typesouscripteur', verbose_name='Type de Souscripteur')),
            ],
            options={
                'verbose_name': 'Souscripteur Physique',
                'verbose_name_plural': 'Souscripteurs Physiques',
            },
        ),
        migrations.CreateModel(
            name='SouscripteurMorale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raison_sociale', models.CharField(max_length=200, verbose_name='Raison Sociale')),
                ('forme_juridique', models.CharField(choices=[('SA', 'SA'), ('SARL', 'SARL'), ('SAS', 'SAS'), ('AUTRE', 'Autre')], max_length=20, verbose_name='Forme Juridique')),
                ('rccm', models.CharField(blank=True, max_length=50, null=True, verbose_name='RCCM')),
                ('ifu', models.CharField(blank=True, max_length=50, null=True, verbose_name='IFU')),
                ('siege_social', models.CharField(max_length=200, verbose_name='Siège Social')),
                ('nom_representant', models.CharField(max_length=100, verbose_name='Nom du Représentant')),
                ('prenom_representant', models.CharField(max_length=100, verbose_name='Prénom du Représentant')),
                ('fonction_representant', models.CharField(max_length=100, verbose_name='Fonction du Représentant')),
                ('telephone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('pays', models.CharField(choices=[('Burkina Faso', 'Burkina Faso'), ("Côte d'Ivoire", "Côte d'Ivoire"), ('Sénégal', 'Sénégal'), ('Mali', 'Mali'), ('Niger', 'Niger'), ('Togo', 'Togo'), ('Bénin', 'Bénin'), ('Guinée', 'Guinée'), ('Ghana', 'Ghana'), ('Nigéria', 'Nigéria'), ('Algérie', 'Algérie'), ('Afrique du Sud', 'Afrique du Sud'), ('Congo (RDC)', 'Congo (RDC)'), ('Kenya', 'Kenya'), ('Maroc', 'Maroc'), ('Tunisie', 'Tunisie'), ('Égypte', 'Égypte'), ('Tanzanie', 'Tanzanie'), ('Zambie', 'Zambie'), ('Ouganda', 'Ouganda')], max_length=100, verbose_name='Pays')),
                ('region', models.CharField(max_length=100, verbose_name='Région')),
                ('ville', models.CharField(max_length=100, verbose_name='Ville')),
                ('adresse', models.TextField(verbose_name='Adresse')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de Création')),
                ('type_souscripteur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='souscriptions.typesouscripteur', verbose_name='Type de Souscripteur')),
            ],
            options={
                'verbose_name': 'Souscripteur Moral',
                'verbose_name_plural': 'Souscripteurs Moraux',
            },
        ),
    ]
