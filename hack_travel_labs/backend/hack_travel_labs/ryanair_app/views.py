from rest_framework import viewsets
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from .exceptions import NoVideoIdGiven
from . import utils
from .models import Video
from .serializers import VideoSerializer


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()


@api_view(['GET'])
@schema(None)
def get_results(request):
    video_id = request.GET.get('video_id')
    if not video_id:
        raise NoVideoIdGiven()
    video = Video.objects.get(id=video_id)

    locations = list()
    for frame in video.frames.all():
        country = frame.flight['outbound']['arrivalAirport']['countryName']
        price = frame.flight['outbound']['price']['value']
        departureAirport = frame.flight['outbound']['departureAirport']['iataCode']
        arrivalAirport = frame.flight['outbound']['arrivalAirport']['iataCode']
        departureDate = frame.flight['outbound']['departureDate'][0:10]
        arrivalDate = frame.flight['outbound']['arrivalDate'][0:10]
        locations.append(dict(
            time=frame.time,
            banner1=utils.banner1(country, price),
            banner2=utils.banner2(country, price),
            link=f'https://www.ryanair.com/pl/pl/booking/home/{departureAirport}/{arrivalAirport}/{departureDate}/{arrivalDate}/1'
        ))
    return Response(data={
        'locations': locations
    }, status=200)
