# Generated by Django 5.1.4 on 2025-01-16 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('souscriptions', '0004_souscriptioneffectuee_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='souscripteurmorale',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, help_text='Date et heure exactes de la création du souscripteur', verbose_name='Date et Heure de Création'),
        ),
        migrations.AlterField(
            model_name='souscripteurphysique',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, help_text='Date et heure exactes de la création du souscripteur', verbose_name='Date et Heure de Création'),
        ),
        migrations.AlterField(
            model_name='souscriptioneffectuee',
            name='date_paiement',
            field=models.DateTimeField(auto_now_add=True, help_text="Date et heure exactes de l'enregistrement du paiement", verbose_name='Date et Heure de Paiement'),
        ),
        migrations.AlterField(
            model_name='souscriptioneffectuee',
            name='date_souscription',
            field=models.DateTimeField(auto_now_add=True, help_text="Date et heure exactes de l'enregistrement de la souscription", verbose_name='Date et Heure de Souscription'),
        ),
        migrations.AlterField(
            model_name='typesouscripteur',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, help_text='Date et heure exactes de la création du type de souscripteur', verbose_name='Date et Heure de Création'),
        ),
    ]
