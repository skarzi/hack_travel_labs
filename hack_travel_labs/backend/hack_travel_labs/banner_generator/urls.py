from django.urls import (
    path,
    register_converter,
)

from . import views

app_name = 'banner_generator'


class FloatConventer:
    regex = r'[0-9]*(\.[0-9]*)?'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

register_converter(FloatConventer, 'float')

urlpatterns = [
    path(
        '<str:city>/<float:price>',
        views.BannerGeneratorView.as_view(),
        name='banner-generator',
    )
]
