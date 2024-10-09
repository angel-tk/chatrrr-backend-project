from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from base.api.serializers import RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/rooms/',
        'GET /api/rooms/:id/',
        'POST /api/rooms/',
        'PUT /api/rooms/:id/',
        'DELETE /api/rooms/:id/',
    ]
    return Response(routes)
