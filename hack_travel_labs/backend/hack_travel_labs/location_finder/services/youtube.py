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
    VideoFrame,
    Video,
)
from hack_travel_labs.location_finder.exceptions import GoogleCloudVisionException


def prepare_video_for_frame_splitting(video):
    part_time = settings.SECONDS_PER_PART
    duration = video.duration
    parts = list()
    part_start = 0
    part_end = min(duration, part_time)
    while part_start < duration:
        parts.append((part_start, part_end))
        part_start, part_end = part_end, min(duration, part_end + part_time)
    return parts


def fill_video_frame_location_data(video_frame, location_service):
    try:
        location_data = location_service.find(video_frame.image.file)
    except GoogleCloudVisionException:
        video_frame.delete()
        return None
    else:
        video_frame.latitude = location_data['coordinates']['latitude']
        video_frame.longtitude = location_data['coordinates']['longtitude']
        video_frame.name = location_data['name']
        video_frame.save()
        return video_frame


def drop_duplicate_locations_by_name(video):
    unique_frames = dict()
    for video_frame in video.frames.all():
        if video_frame.name in unique_frames:
            video_frame.delete()
        else:
            unique_frames.setdefault(video_frame.name, video_frame)
    video.frames.set(list(unique_frames.values()))
    video.save()
    return video


class YouTubeVideoDataExtractService:
    def __init__(self, resolution='hd720'):
        self._resolution = resolution

    def extract(self, video_url):
        with youtube_dl.YoutubeDL() as ytdl:
            video_info = ytdl.extract_info(video_url, download=False)
            video_url = self._get_resolution_url(video_info['formats'])
            if not video_url:
                raise ValueError('missing hd resolution')
            return Video.objects.create(
                id=video_info['id'],
                duration=video_info['duration'],
                url=video_url,
            )

    def _get_resolution_url(self, formats):
        for format_details in formats:
            if (self._is_video(format_details)
                    and format_details.get('format_note') == self._resolution):
                return format_details['url']
        return None

    @staticmethod
    def _is_video(format_details):
        return not ('format_note' not in format_details
                    or 'url' not in format_details)


class VideoFrameExtractService:
    def extract(self, video, start=0, stop=None):
        stop = stop or video.duration
        frames = list()
        for frame_file in self._extract_frames_to_files(video, start, stop):
            frames.append(VideoFrame(
                video=video,
                image=frame_file,
                time=self._excel_frame_time(frame_file, video.frequency),
            ))
        VideoFrame.objects.bulk_create(frames)
        return frames

    @staticmethod
    def _extract_frames_to_files(video, start, stop):
        subprocess.call([
            'ffmpeg',
            # '-ss', str(start), '-t', str(stop - start),
            '-i', video.url,
            '-stats',
            '-vframes', str(int(video.duration * video.frequency)),
            '-r', str(video.frequency),
            '-hide_banner',
            '-loglevel', 'warning',
            '-q:v', '2',
            os.path.join(
                video.frames_directory,
                f'%0{settings.FRAMES_FILENAME_LENGTH}d.jpg',
            ),
        ])
        return glob.glob(os.path.join(video.frames_directory, "*.jpg"))

    @staticmethod
    def _excel_frame_time(frame_name, frequency):
        length = settings.FRAMES_FILENAME_LENGTH
        extension_length = 4
        frame_index = frame_name[-(length+extension_length):-extension_length]
        return int((int(frame_index) - 1) / frequency)
