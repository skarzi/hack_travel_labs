import os
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('hack_travel_labs')


class CeleryConfig(AppConfig):
    name = 'hack_travel_labs.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        if hasattr(settings, 'RAVEN_CONFIG'):   # pragma: no cover
            # Celery signal registration

            # Since raven is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.

            # @formatter:off

            from raven import Client # pylint: disable=E0401, pragma: no cover
            from raven.contrib.celery import register_signal # pylint: disable=E0401, pragma: no cover
            from raven.contrib.celery import register_logger_signal # pylint: disable=E0401, pragma: no cover

            # @formatter:on

            raven_client = Client(dsn=settings.RAVEN_CONFIG['DSN']) # pragma: no cover
            register_logger_signal(raven_client)  # pragma: no cover
            register_signal(raven_client) # pragma: no cover


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover
