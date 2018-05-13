from rest_framework.views import APIView
from rest_framework.response import Response

from hack_travel_labs.ryanair_app.serializers import VideoSerializer
from hack_travel_labs.ryanair_app.models import Video
from hack_travel_labs.flight_finder import tasks
from hack_travel_labs.ryanair_app.tasks import results

from .services import (
    drop_duplicate_locations_by_name,
    fill_video_frame_location_data,
    GoogleLocationService,
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
        try:
            video = Video.objects.get(pk=video_url[-11:])
        except Video.DoesNotExist:
            pass
        else:
            self.search_flight_again(video, request)
            return Response(data=VideoSerializer(video).data)
        print(f'getting data for {video_url}...')
        video = YouTubeVideoDataExtractService().extract(video_url)
        print(f'data for {video.id}: {video.duration}, {video.frequency}')
        location_service = GoogleLocationService()
        video_frame_extract_service = VideoFrameExtractService()
        # parts = prepare_video_for_frame_splitting(video)
        for i, video_frame in enumerate(
            video_frame_extract_service.extract(video),
        ):
            if i % 7 == 0:
                fill_video_frame_location_data(video_frame, location_service)
            else:
                video_frame.delete()
        video = drop_duplicate_locations_by_name(video)
        self.search_flight_again(video, request)
        location = results(request, video.id)
        return Response(data={
            'location': location
        }, status=200)

    @staticmethod
    def search_flight_again(video, request):
        for video_frame in video.frames.all():
            flight = tasks.find_flight(dict(
                ip='213.216.126.33',
                lat=video_frame.latitude,
                lng=video_frame.longtitude,
                forth_depart=request.GET.get('forth_depart', '2018-05-12'),
                forth_arrive=request.GET.get('forth_arrive', '2018-05-15'),
                back_depart=request.GET.get('back_depart', '2018-05-20'),
                back_arrive=request.GET.get('back_arrive', '2018-05-22'),
            ))
            video_frame.flight = flight
            video_frame.save()

    def _get_image_or_raise(self, request):
        try:
            return request.FILES[self.image_file_key]
        except KeyError:
            raise MissingImageException(image_key=self.image_file_key)
