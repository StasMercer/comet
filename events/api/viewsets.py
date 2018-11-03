from rest_framework import generics
from rest_framework import viewsets
from events.models import Event, Tag
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

