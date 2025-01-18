import threading
import time
from django.utils import timezone
from django.db import connection
import logging
from operations.models import ListesParcelles

logger = logging.getLogger(__name__)

class ParcelleDeblocageThread:
    _instance = None
    _thread = None
    _stop_event = None
    _last_check = None
    CHECK_INTERVAL = 60  # Intervalle de vérification en secondes (1 minute)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._stop_event = threading.Event()
        self._thread = None
        self._last_check = None

    def debloquer_parcelles_expirees(self):
        print("Thread de déblocage démarré et en cours d'exécution...")
        while not self._stop_event.is_set():
            try:
                now = timezone.now()
                
                # Éviter les vérifications trop rapprochées
                if self._last_check and (now - self._last_check).total_seconds() < self.CHECK_INTERVAL:
                    time.sleep(1)
                    continue
                
                self._last_check = now
                print(f"Vérification des parcelles expirées à {now}")
                
                # Fermer et rouvrir la connexion
                connection.close()
                
                # Récupérer les parcelles dont le blocage est expiré
                parcelles_expirees = ListesParcelles.objects.filter(
                    bloquer=True,
                    paye=False,
                    date_blocage__isnull=False,
                    date_fin_blocage__isnull=False,
                    date_fin_blocage__lte=now
                ).select_for_update()
                
                nb_parcelles = parcelles_expirees.count()
                print(f"Nombre de parcelles à débloquer : {nb_parcelles}")

                if nb_parcelles > 0:
                    for parcelle in parcelles_expirees:
                        try:
                            temps_restant = (parcelle.date_fin_blocage - now).total_seconds()
                            print(f"""
                                Déblocage de la parcelle {parcelle.id}:
                                - Date de blocage: {parcelle.date_blocage}
                                - Date de fin prévue: {parcelle.date_fin_blocage}
                                - Date actuelle: {now}
                                - Temps dépassé: {-temps_restant} secondes
                            """)
                            
                            parcelle.bloquer = False
                            parcelle.date_blocage = None
                            parcelle.date_fin_blocage = None
                            parcelle.save()
                            
                            print(f"Parcelle {parcelle.id} débloquée avec succès")
                            logger.info(f"""
                                Parcelle {parcelle.id} débloquée automatiquement:
                                - Débloquée à: {now}
                                - Était bloquée depuis: {parcelle.date_blocage}
                                - Devait expirer à: {parcelle.date_fin_blocage}
                            """)
                        except Exception as e:
                            print(f"Erreur lors du déblocage de la parcelle {parcelle.id}: {str(e)}")
                            logger.error(f"Erreur lors du déblocage de la parcelle {parcelle.id}: {str(e)}")

            except Exception as e:
                print(f"Erreur dans le thread de déblocage: {str(e)}")
                logger.error(f"Erreur dans le thread de déblocage: {str(e)}")
            finally:
                connection.close()
            
            # Attendre 1 minute avant la prochaine vérification
            time.sleep(self.CHECK_INTERVAL)

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            print("Démarrage du thread de déblocage...")
            self._stop_event.clear()
            self._thread = threading.Thread(target=self.debloquer_parcelles_expirees, daemon=True)
            self._thread.start()
            print("Thread de déblocage démarré avec succès")
            logger.info("Thread de déblocage des parcelles démarré")

    def stop(self):
        if self._thread and self._thread.is_alive():
            print("Arrêt du thread de déblocage...")
            self._stop_event.set()
            self._thread.join()
            print("Thread de déblocage arrêté")
            logger.info("Thread de déblocage des parcelles arrêté") 