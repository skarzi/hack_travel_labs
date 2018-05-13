from . import utils
from .models import Video


def results(request, video_id):
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

    return location


def _make_url(request, banner):
    return f'http://{request.META["HTTP_HOST"]}{banner}'
