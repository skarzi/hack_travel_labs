from rest_framework import serializers

from .models import VideoFrame, Video


class VideoFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFrame
        fields = ['name', 'time', 'latitude', 'longtitude', 'flight']


class VideoSerializer(serializers.ModelSerializer):
    locations = VideoFrameSerializer(source='frames', many=True)

    class Meta:
        model = Video
        fields = ['id', 'locations']
