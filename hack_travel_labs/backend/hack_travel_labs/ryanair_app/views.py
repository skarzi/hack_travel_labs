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

    location = None
    for frame in video.frames.all():
        if frame.flight != 'Not found':
            country = frame.flight['outbound']['arrivalAirport']['countryName']
            price = frame.flight['outbound']['price']['value']
            departureAirport = frame.flight['outbound']['departureAirport']['iataCode']
            arrivalAirport = frame.flight['outbound']['arrivalAirport']['iataCode']
            departureDate = frame.flight['outbound']['departureDate'][0:10]
            arrivalDate = frame.flight['outbound']['arrivalDate'][0:10]
            location = dict(
                time=frame.time,
                banner1=_make_url(request, utils.banner1(country, price)),
                banner2=_make_url(request, utils.banner2(country, price)),
                link=f'https://www.ryanair.com/pl/pl/booking/home/{departureAirport}/{arrivalAirport}/{departureDate}/{arrivalDate}/1'
            )
            break
    return Response(data={
        'location': location
    }, status=200)


def _make_url(request, banner):
    return f'http://{request.META["HTTP_HOST"]}{banner}'
