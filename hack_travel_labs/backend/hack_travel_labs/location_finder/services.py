import os
import glob
import subprocess

from collections import defaultdict

import youtube_dl

from django.conf import settings
from google.cloud.vision import (
    ImageAnnotatorClient,
    types,
)

from hack_travel_labs.ryanair_app.models import (
    ImageFrame,
    Video,
)

from .exceptions import GoogleCloudVisionException


class YouTubeVideoProcessor:
    def __call__(self, *args, **kwargs):
        return self.process(*args, **kwargs)

    def process(self, video_url, location_finder, context=None):
        context = context or dict()
        video_id, frame_duration, frame_glob = self.save_frames(
            video_url,
            context,
        )
        locations = self.find_locations(
            frame_glob, location_finder, context, frame_duration, fast=True,
        )
        if len(locations) == 0:
            locations = self.find_locations(
                frame_glob, location_finder, context, frame_duration, fast=False,
            )
        tmp = [(location[0], len(location))
               for location in locations.values()]
        locations = sorted(tmp, key=lambda x: x[-1], reverse=True)
        locations = [location[0] for location in locations]
        video = Video.objects.create(id=video_id)
        ImageFrame.objects.bulk_create([
            self._make_image_frame(video, location)
            for location in locations
        ])
        return {'locations': locations}

    def _make_image_frame(self, video, location):
        return ImageFrame(
            video=video,
            name=location['name'],
            timestamp=location['seconds'],
            lat=location['coordinates']['latitude'],
            lng=location['coordinates']['longtitude'],
        )

    def save_frames(self, video_url, context):
        frames_per_video = context.get('frames', settings.FRAMES_PER_VIDEO)
        with youtube_dl.YoutubeDL() as ytdl:
            data = ytdl.extract_info(video_url, download=False)
            video_directory = os.path.join(
                settings.FRAMES_DIRECTORY,
                data['id'],
            )
            if not os.path.exists(video_directory):
                os.makedirs(video_directory)
            duration = data['duration']
            video_url = self._get_resolution_url(data['formats'])
            if not video_url:
                raise ValueError('missing hd resolution')
            hz = max(min(frames_per_video / duration, 1), 0.1)
            return (
                data['id'],
                1 / hz,
                self._extract_frames(
                    video_url,
                    duration,
                    hz,
                    video_directory,
                ),
            )

    def find_locations(
        self, frame_glob, location_finder, context, frame_duration, fast=False,
    ):
        check_func = lambda index: index % 10 != 0
        if fast:
            check_func = lambda index: index % 10 == 0
        locations = defaultdict(list)
        for i, frame_file in enumerate(frame_glob):
            if check_func(i):
                continue
            with open(frame_file, 'rb') as f:
                try:
                    location = location_finder(f, context)
                except GoogleCloudVisionException:
                    pass
                else:
                    location['seconds'] = self._get_location_seconds(
                        frame_file,
                        frame_duration,
                    )
                    locations[location['name']].append(location)
        return locations

    def _get_resolution_url(self, formats, resolution='hd720'):
        for format_details in formats:
            if (self._is_video(format_details)
                    and format_details.get('format_note') == resolution):
                return format_details['url']
        return None

    def _is_video(self, format_details):
        return not ('format_note' not in format_details
                    or 'url' not in format_details)

    def _extract_frames(self, url, duration, hz, directory):
        subprocess.call([
            'ffmpeg', '-i', url, '-stats', '-vframes',
            str(int(duration * hz)), '-r', str(hz), '-hide_banner', '-loglevel',
            'warning', '-q:v', '2', os.path.join(directory, '%03d.jpg'),
        ])
        return glob.glob(os.path.join(directory, "*.jpg"))

    def _get_location_seconds(self, frame_name, frame_duration):
        return int((int(frame_name[-7:-4]) - 1) * frame_duration)


class GoogleLocationFinder:
    image_annotator = ImageAnnotatorClient()

    def __call__(self, *args, **kwargs):
        return self.find(*args, **kwargs)

    def find(self, image_obj, context=None):
        context = context or dict()
        if hasattr(image_obj, 'file'):
            image_obj = image_obj.file
        image = types.Image(content=image_obj.read())
        response = self.image_annotator.landmark_detection(image)
        self._raise_for_error(response)
        return self._make_response(response.landmark_annotations)

    def _make_response(self, landmark_annotations):
        try:
            landmark = landmark_annotations[0]
        except IndexError:
            raise GoogleCloudVisionException(detail='Landmark not found.')
        return self._landmark_annotation_to_dict(landmark)

    def _raise_for_error(self, response):
        if response.HasField('error'):
            raise GoogleCloudVisionException(
                detail=response.error.message,
            )

    def _landmark_annotation_to_dict(self, landmark_annotation):
        try:
            coordinates = landmark_annotation.locations[0].lat_lng
        except IndexError:
            raise GoogleCloudVisionException(detail='Location not found.')
        return {
            'coordinates': {
                'latitude': coordinates.latitude,
                'longtitude': coordinates.longitude,
            },
            'name': landmark_annotation.description,
        }
