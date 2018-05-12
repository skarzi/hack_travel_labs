from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .services import GoogleLocationFinder
from .exceptions import MissingImageException


class LocationFindView(APIView):
    permission_classes = (AllowAny,)
    image_file_key = 'image'

    def post(self, request):
        image = self._get_image_or_raise(request)
        location_finder = GoogleLocationFinder()
        return Response(data=location_finder.find(image, {'context': request}))

    def _get_image_or_raise(self, request):
        try:
            return request.FILES[self.image_file_key]
        except KeyError:
            raise MissingImageException(image_key=self.image_file_key)
