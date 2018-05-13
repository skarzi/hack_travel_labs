from django.apps import AppConfig


class BannerGeneratorConfig(AppConfig):
    name = 'hack_travel_labs.banner_generator'
    verbose_name = "Banner Generator"

    def ready(self):
        """Override this to put in:
            Banner Generator system checks
            Banner Generator signal registration
        """
        pass
