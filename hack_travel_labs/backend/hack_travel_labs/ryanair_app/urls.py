from django.conf.urls import include, url
from rest_framework import routers

from . import views


app_name = 'ryanair'

router = routers.DefaultRouter()
router.register(r'image_frames', views.ImageFrameViewSet, base_name='image_frames')

urlpatterns = [
    url(r'^$', include(router.urls)),
]
