from django.apps import AppConfig
from django.conf import settings

class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"
    
    def ready(self):
        import apps.dashboard.signals
