from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Tracks
from .serializers import TracksSerializer

@api_view(['GET'])
def tracks_list(request):
    tracks = Tracks.objects.using('questdb').all()
    serializer = TracksSerializer(tracks, many=True)
    return Response(serializer.data)