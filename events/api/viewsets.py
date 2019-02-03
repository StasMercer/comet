from datetime import date

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination

from comet.permissions import IsOwner
from events.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.api.serializers import ShortUserSerializer


class EventRegisterViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventRegisterSerializer
    http_method_names = ['post']

    def get_permissions(self):
        return (IsAuthenticated(),)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get', 'patch']


    def get_permissions(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT':
            return (IsOwner(),)
        else:
            return (IsAuthenticated(),)

    @action(detail=True, methods=['get'],)
    def get_members(self, request, pk):
        event = Event.objects.get(pk=pk)
        return Response(ShortUserSerializer(event.members, many=True).data)

    """just {"username":"your_username"}"""
    @action(detail=True, methods=['patch'])
    def add_follower(self, request, pk=None):

        event = Event.objects.get(pk=pk)
        try:
            username = request.data['username']
            user = CustomUser.objects.get(username=username)
            event.members.add(user)
            return Response('ok')
        except CustomUser.DoesNotExist:
            return Response('user_does_not_exist')
        except KeyError:
            return Response('no_appropriate_arguments')

    """just {"username":"your_username"}"""
    @action(detail=True, methods=['patch'])
    def remove_follower(self, request, pk=None):

        event = Event.objects.get(pk=pk)
        try:
            username = request.data['username']
            user = CustomUser.objects.get(username=username)
            event.members.remove(user)
            return Response('ok')
        except CustomUser.DoesNotExist:
            return Response('user_does_not_exist')
        except KeyError:
            return Response('no_appropriate_arguments')

    @action(detail=False, methods=['get'])
    def get_not_expired(self, request):
        queryset = Event.objects.filter(date_expire__gt=date.today())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

