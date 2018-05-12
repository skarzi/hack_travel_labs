from rest_framework import viewsets

from .models import ImageFrame
from .serializers import ImageFrameSerializers


class ImageFrameViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ImageFrameSerializers
    queryset = ImageFrame.objects.all()
