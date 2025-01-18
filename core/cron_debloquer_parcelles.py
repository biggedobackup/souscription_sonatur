from django.core.management.base import BaseCommand
from django.utils import timezone
from operations.models import ListesParcelles
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Débloque automatiquement les parcelles dont le temps de réservation est expiré'

    def handle(self, *args, **options):
        try:
            parcelles_bloquees = ListesParcelles.objects.filter(
                bloquer=True,
                date_blocage__isnull=False,
                date_fin_blocage__lte=timezone.now(),
                paye=False  # Ne pas débloquer les parcelles payées
            )
            
            count = parcelles_bloquees.count()
            
            for parcelle in parcelles_bloquees:
                parcelle.bloquer = False
                parcelle.date_blocage = None
                parcelle.date_fin_blocage = None
                parcelle.save()
                logger.info(f"Parcelle {parcelle.id} débloquée automatiquement")
            
            self.stdout.write(
                self.style.SUCCESS(f'{count} parcelles débloquées avec succès')
            )
            
        except Exception as e:
            logger.error(f"Erreur lors du déblocage des parcelles: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f'Erreur: {str(e)}')
            )