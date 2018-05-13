from rest_framework import viewsets
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response

from .tasks import results
from .exceptions import NoVideoIdGiven
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

    location = results(request, video_id)

    return Response(data={
        'location': location
    }, status=200)
