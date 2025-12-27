from django.apps import AppConfig


class AneesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "anees"

    def ready(self):
        import anees.signals
