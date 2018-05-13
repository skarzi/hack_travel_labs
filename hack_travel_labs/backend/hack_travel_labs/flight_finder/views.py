from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    schema,
)

from hack_travel_labs.ryanair_app.serializers import VideoSerializer

from .tasks import find_flight
from .exceptions import (
    InvalidEnvironment,
    MissingLatParam,
    MissingLngParam,
)


@api_view(['GET'])
@schema(None)
def get_flights_for_lat_lng(request):
    # Example lat: 51.50853
    # Example long: -0.12574
    # Example ip: 213.216.126.33
    if settings.ENVIRONMENT == 'PRODUCTION':
        ip = request.META.get('REMOTE_ADDR', '213.216.126.33')
    elif settings.ENVIRONMENT == 'LOCAL':
        ip = '213.216.126.33'
    else:
        raise InvalidEnvironment()

    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    url = request.GET.get('url')
    """
    if not lat:
        raise MissingLatParam()
    elif not lng:
        raise MissingLngParam()
    """

    flight = find_flight(dict(
        video_url=url,
        ip=ip,
        lat=lat,
        lng=lng,
        forth_depart=request.GET.get('forth_depart', '2018-05-12'),
        forth_arrive=request.GET.get('forth_arrive', '2018-05-15'),
        back_depart=request.GET.get('back_depart', '2018-05-20'),
        back_arrive = request.GET.get('back_arrive', '2018-05-22'),
    ))

    return Response(data={
        'flight': VideoSerializer(flight)
    }, status=200)
