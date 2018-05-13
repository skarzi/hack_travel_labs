from hack_travel_labs.location_finder import services

from . import utils


# TODO:
# separate celery tasks for:
# + splitting video into frames
# + searching location
# + calling ryanair API for location
#
# Then isplit video into parts and start pipeline e.g for each 2 minutes of
# film
def find_flight(context):
    context.setdefault('location_finder', services.GoogleLocationFinder())
    yt_video_processor = services.YouTubeVideoProcessor()
    video = yt_video_processor(context)
    sources = utils.find_nearby_airports_by_ip(context.get('ip'))
    for location in video.locations.all():
        destinations = utils.find_nearby_airports_by_lat_lng(
            location.lat,
            location.lng,
        )
        flight = utils.find_cheapest_flight(sources, destinations, context)
        location.flight = flight
        location.save()
    return video
