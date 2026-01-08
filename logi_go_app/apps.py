from django.apps import AppConfig

class LogiGoAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logi_go_app'

    def ready(self):
        # Import the signals module here
        import logi_go_app.signals
