from django.conf.urls import url

from . import views


app_name = 'users'


urlpatterns = [
    url(
        regex=r'^$',
        view=views.get_flights_for_lat_lng,
        name='flights'
    ),
]
