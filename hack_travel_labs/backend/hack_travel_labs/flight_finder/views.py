from django.conf import settings
from rest_framework import permissions
from rest_framework.decorators import api_view, schema, permission_classes
from rest_framework.response import Response

from .exceptions import InvalidEnvironment
from . import utils

@api_view(['GET'])
@permission_classes([permissions.AllowAny,])
@schema(None)
def get_flights_for_lat_lng(request):
    # Example lat: 51.50853
    # Example long: -0.12574
    # Example ip: 213.216.126.33
    if settings.ENVIRONMENT == 'PRODUCTION':
        ip = request.META.get('REMOTE_ADDR')
    elif settings.ENVIRONMENT == 'LOCAL':
        ip = '213.216.126.33'
    else:
        raise InvalidEnvironment()
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    sources = utils.find_nearby_airports_by_ip(ip)
    destinations = utils.find_nearby_airports_by_lat_lng(lat, lng)
    flight = utils.find_cheapest_flight(sources, destinations)
    return Response(data={
        'flight': flight
    }, status=200)
