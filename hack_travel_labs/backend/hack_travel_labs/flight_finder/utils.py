import requests
from django.conf import settings
from funcy import first

from .exceptions import NoFlightFoundFound


def request_ryanair(url, args):
    base_url = 'http://apigateway.ryanair.com/pub/v1'
    auth = 'apikey={}'.format(settings.RYANAIR_KEY)
    response = requests.get(f'{base_url}/{url}?{args}&{auth}')
    response.raise_for_status()
    return response.json()

def find_nearby_airports_by_ip(ip):
    return _find_nearby_airports(f'ip={ip}')

def find_nearby_airports_by_lat_lng(lat, lng):
    return _find_nearby_airports(f'latitude={lat}&longitude={lng}')

def _find_nearby_airports(args):
    args = f'{args}&limit=10'
    return request_ryanair('geolocation/3/nearbyAirports', args)

def find_cheapest_flight(sources, destinations):
    for destination in destinations:
        destination_loc = destination.get('iataCode')
        for source in sources:
            source_loc = source.get('iataCode')
            args = f'departureAirportIataCode={source_loc}&arrivalAirportIataCode={destination_loc}'
            forth_depart = '2018-05-12'
            forth_arrive = '2018-05-15'
            args = f'{args}&outboundDepartureDateFrom={forth_depart}&outboundDepartureDateTo={forth_arrive}'
            back_depart = '2018-05-20'
            back_arrive = '2018-05-22'
            args = f'{args}&inboundDepartureDateFrom={back_depart}&inboundDepartureDateTo={back_arrive}'
            try:
                cheapest_flight = _find_cheapest_flight(args)
                return cheapest_flight
            except NoFlightFoundFound:
                continue
    return 'Not found'

def _find_cheapest_flight(args):
    flights = request_ryanair('farefinder/3/roundTripFares', args)
    if not flights.get('total'):
        raise NoFlightFoundFound()
    return first(flights.get('fares'))
