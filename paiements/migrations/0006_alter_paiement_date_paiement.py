# Generated by Django 5.1.4 on 2025-01-16 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paiements', '0005_remove_paiement_numero_paiement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paiement',
            name='date_paiement',
            field=models.DateTimeField(auto_now_add=True, help_text="Date et heure exactes de l'enregistrement du paiement", verbose_name='Date et Heure du Paiement'),
        ),
    ]
