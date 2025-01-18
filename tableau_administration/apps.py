from django.apps import AppConfig

class TableauAdministrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tableau_administration'

    def ready(self):
        # Éviter le double démarrage avec le reloader
        import os
        if os.environ.get('RUN_MAIN', None) != 'true':
            from .parcelle_thread import ParcelleDeblocageThread
            thread = ParcelleDeblocageThread.get_instance()
            thread.start()
    
