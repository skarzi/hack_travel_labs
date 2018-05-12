from django.conf import settings
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from .exceptions import InvalidEnvironment, MissingLatParam, MissingLngParam
from . import utils

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
    if not lat:
        raise MissingLatParam()
    elif not lng:
        raise MissingLngParam()

    params = dict(
        forth_depart=request.GET.get('forth_depart', '2018-05-12'),
        forth_arrive=request.GET.get('forth_arrive', '2018-05-15'),
        back_depart=request.GET.get('back_depart', '2018-05-20'),
        back_arrive = request.GET.get('back_arrive', '2018-05-22'),
    )

    sources = utils.find_nearby_airports_by_ip(ip)
    destinations = utils.find_nearby_airports_by_lat_lng(lat, lng)
    flight = utils.find_cheapest_flight(sources, destinations, params)
    return Response(data={
        'flight': flight
    }, status=200)
