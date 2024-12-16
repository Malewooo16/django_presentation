from django.apps import AppConfig





class MyAppConfig(AppConfig):
    name = 'inventory'

    def ready(self):
        # Automatically assign the permissions when the app is ready
        import inventory.signals
