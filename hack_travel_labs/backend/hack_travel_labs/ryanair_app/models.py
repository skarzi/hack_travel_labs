from django.contrib.postgres.fields import JSONField
from django.db import models


class Video(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    flight = JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.id}'


class ImageFrame(models.Model):
    name = models.CharField(max_length=255, default='')
    timestamp = models.PositiveIntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='frames',
    )

    def __str__(self):
        return f'{self.name}({self.lat}, {self.lng})'
