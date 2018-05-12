from rest_framework import serializers

from .models import ImageFrame


class ImageFrameSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageFrame
        fields = '__all__'
