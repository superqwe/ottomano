from django.apps import AppConfig


class SgiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sgi'

    def ready(self):
        import sgi.signals
