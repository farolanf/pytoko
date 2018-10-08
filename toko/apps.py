from django.apps import AppConfig

class TokoConfig(AppConfig):
    name = 'toko'

    def ready(self):
        import toko.receivers