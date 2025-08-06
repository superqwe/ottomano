from django.apps import AppConfig


class PersonaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personale'

    def ready(self):
        import personale.signals
