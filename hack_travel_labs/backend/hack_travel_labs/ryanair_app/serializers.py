from rest_framework import serializers

from .models import ImageFrame, Video


class ImageFrameSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageFrame
        fields = ['name', 'timestamp', 'lat', 'lng']


class VideoSerializers(serializers.ModelSerializer):
    locations = ImageFrameSerializers(source='frames', many=True)

    class Meta:
        model = Video
        fields = ['id', 'flight', 'locations']
