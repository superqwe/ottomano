from django.apps import AppConfig


class MezziConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mezzi'

    def ready(self):
        import mezzi.signals