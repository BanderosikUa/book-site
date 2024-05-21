from django.apps import AppConfig


class GenresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'genres'

    def ready(self):
        from . import signals
