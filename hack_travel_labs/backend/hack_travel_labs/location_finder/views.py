from rest_framework.views import APIView
from rest_framework.response import Response

from hack_travel_labs.ryanair_app.serializers import VideoSerializer

from .services import (
    fill_video_frame_location_data,
    GoogleLocationService,
    prepare_video_for_frame_splitting,
    VideoFrameExtractService,
    YouTubeVideoDataExtractService,
)
from .exceptions import MissingImageException


class LocationFindView(APIView):
    image_file_key = 'image'

    def post(self, request):
        image = self._get_image_or_raise(request)
        location_service = GoogleLocationService()
        return Response(data=location_service.find(image))

    def get(self, request):
        video_url = request.query_params['video_url']
        print(f'getting data for {video_url}...')
        video = YouTubeVideoDataExtractService().extract(video_url)
        print(f'data for {video.id}: {video.duration}, {video.frequency}')
        location_service = GoogleLocationService()
        video_frame_extract_service = VideoFrameExtractService()
        # parts = prepare_video_for_frame_splitting(video)
        for video_frame in video_frame_extract_service.extract(video):
            fill_video_frame_location_data(video_frame, location_service)
        return Response(data=VideoSerializer(video).data)

    def _get_image_or_raise(self, request):
        try:
            return request.FILES[self.image_file_key]
        except KeyError:
            raise MissingImageException(image_key=self.image_file_key)
