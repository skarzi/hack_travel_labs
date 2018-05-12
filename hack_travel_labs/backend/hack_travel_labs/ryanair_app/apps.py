from django.apps import AppConfig


class RyanairConfig(AppConfig):
    name = 'hack_travel_labs.ryanair_app'
    verbose_name = 'Ryanair'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
