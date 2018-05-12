import pytest
from pytest_django.lazy_django import skip_if_no_django
from requests_mock import MockerCore
from faker import config
from rest_framework.test import APIRequestFactory


config.DEFAULT_LOCALE = 'pl_PL'


@pytest.fixture(scope='session')
def faker_locale():
    return 'pl_PL'


def setup_view(view, request, *args, **kwargs):
    """
    Mimic as_view() returned callable, but returns view instance.
    args and kwargs are the same you would pass to ``reverse()``

    Example:
    name = 'django'
    request = RequestFactory().get('/fake-path')
    view = HelloView(template_name='hello.html')
    view = setup_view(view, request, name=name)

    Example test ugly dispatch():
    response = view.dispatch(view.request, *view.args, **view.kwargs)
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


def api_setup_view(view, request, action, *args, **kwargs):
    """
    request = HttpRequest()
    view = views.ProfileInfoView()
    view = api_setup_view(view, request, 'list')
    assert view.get_serializer_class() == view.serializer_class
    """
    view.request = request
    view.action = action
    view.args = args
    view.kwargs = kwargs
    return view


@pytest.fixture()
def api_rf():
    """APIRequestFactory instance"""
    skip_if_no_django()
    return APIRequestFactory()


@pytest.yield_fixture(scope="session")
def requests_mock():
    mock = MockerCore()
    mock.start()
    yield mock
    mock.stop()
