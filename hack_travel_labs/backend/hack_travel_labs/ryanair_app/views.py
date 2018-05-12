from rest_framework import viewsets

from .models import Video
from .serializers import VideoSerializers


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializers
    queryset = Video.objects.all()
