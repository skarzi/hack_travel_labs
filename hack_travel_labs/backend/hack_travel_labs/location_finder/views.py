from rest_framework.views import APIView
from rest_framework.response import Response

from .services import (
    GoogleLocationFinder,
    YouTubeVideoProcessor,
)
from .exceptions import MissingImageException


class LocationFindView(APIView):
    image_file_key = 'image'

    def post(self, request):
        image = self._get_image_or_raise(request)
        location_finder = GoogleLocationFinder()
        return Response(data=location_finder.find(image, {'request': request}))

    def get(self, request):
        url = request.query_params['url']
        youtube_processor = YouTubeVideoProcessor()
        location_finder = GoogleLocationFinder()
        return Response(data=youtube_processor(url, location_finder, {'request': request}))

    def _get_image_or_raise(self, request):
        try:
            return request.FILES[self.image_file_key]
        except KeyError:
            raise MissingImageException(image_key=self.image_file_key)
