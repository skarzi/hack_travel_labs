import os

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.contrib.postgres.fields import JSONField


def video_frames_unique_directory(video):
    directory_path = os.path.join(settings.FRAMES_ROOT, video.id)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path


def image_frame_path(instance, filename):
    return os.path.join(
        video_frames_unique_directory(instance.video),
        filename,
    )


class Video(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    url = models.CharField(max_length=747)
    duration = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.id}'

    @cached_property
    def frequency(self):
        return max(min(settings.FRAMES_PER_VIDEO / self.duration, 1), 0.1)

    @cached_property
    def frames_directory(self):
        return video_frames_unique_directory(self)


class VideoFrame(models.Model):
    name = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to=image_frame_path)
    time = models.PositiveIntegerField(null=True)
    latitude = models.FloatField(null=True)
    longtitude = models.FloatField(null=True)
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='frames',
    )
    flight = JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}({self.latitude}, {self.longtitude})'
