from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'business_admin'

    def ready(self):
        """Preload all API permissions when the app starts."""
        from system.permissions import create_permissions
        post_migrate.connect(create_permissions, sender=self)


    