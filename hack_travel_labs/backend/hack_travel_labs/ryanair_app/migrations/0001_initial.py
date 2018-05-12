# Generated by Django 2.0.3 on 2018-05-12 17:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFrame',
            fields=[
                ('video_id', models.CharField(max_length=1024, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=255)),
                ('timestamp', models.PositiveIntegerField()),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('flight', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
    ]
