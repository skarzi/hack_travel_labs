from django.apps import AppConfig


class FlightConfig(AppConfig):
    name = 'hack_travel_labs.flight_finder'
    verbose_name = 'Flights'

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
