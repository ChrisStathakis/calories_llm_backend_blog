from django.apps import AppConfig

class PlaningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'planning'

    def ready(self):
        from . import signals