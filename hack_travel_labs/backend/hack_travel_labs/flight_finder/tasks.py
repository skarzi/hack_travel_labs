from . import utils


def find_flight(context):
    sources = utils.find_nearby_airports_by_ip(context.get('ip'))
    destinations = utils.find_nearby_airports_by_lat_lng(context.get('lat'), context.get('lng'))
    flight = utils.find_cheapest_flight(sources, destinations, context)
    return flight
