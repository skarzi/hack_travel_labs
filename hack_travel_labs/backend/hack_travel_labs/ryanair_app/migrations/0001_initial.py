# Generated by Django 2.0.3 on 2018-05-12 23:27

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import hack_travel_labs.ryanair_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=747)),
                ('duration', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VideoFrame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('image', models.ImageField(upload_to=hack_travel_labs.ryanair_app.models.image_frame_path)),
                ('time', models.PositiveIntegerField(null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longtitude', models.FloatField(null=True)),
                ('flight', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frames', to='ryanair_app.Video')),
            ],
        ),
    ]
