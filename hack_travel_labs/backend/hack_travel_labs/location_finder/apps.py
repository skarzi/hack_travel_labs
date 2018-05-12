from django.apps import AppConfig


class LocationFinderConfig(AppConfig):
    name = 'hack_travel_labs.location_finder'
    verbose_name = "Location Finder"

    def ready(self):
        """Override this to put in:
            Location Finder system checks
            Location Finder signal registration
        """
        pass
