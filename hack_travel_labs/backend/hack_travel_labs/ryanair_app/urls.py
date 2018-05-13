from django.conf.urls import include, url
from rest_framework import routers

from . import views


app_name = 'ryanair'

router = routers.DefaultRouter()
router.register(r'videos', views.VideoViewSet, base_name='videos')

urlpatterns = [
    url(r'', include(router.urls)),
    url(
        regex=r'^results/$',
        view=views.get_results,
        name='results'
    ),
]
