from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from comet.permissions import IsOwner
from events.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return (IsOwner(),)
        else:
            return (IsAuthenticated(),)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

