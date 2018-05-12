from django.contrib.postgres.fields import JSONField
from django.db import models


class ImageFrame(models.Model):
    video_id = models.CharField(max_length=1024, primary_key=True)
    name = models.CharField(max_length=255, default='')
    timestamp = models.PositiveIntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
    flight = JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.video_id}'
