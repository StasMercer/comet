from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import viewsets
from chat.models import Message
from .serializers import  MessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['get'])
    def get_by_event(self, request):

        try:
            event = request.GET['event']
            serializer = MessageSerializer(Message.objects.filter(event_id=event), many=True, read_only=True)
            return Response(serializer.data)
        except MultiValueDictKeyError:
            return Response('event_not_found')
