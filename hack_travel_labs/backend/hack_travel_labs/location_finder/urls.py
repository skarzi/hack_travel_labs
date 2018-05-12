from django.urls import path

from . import views

app_name = 'location_finder'


urlpatterns = [
    path('find/', views.LocationFindView.as_view(), name='location-find')
]
