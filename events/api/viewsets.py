from datetime import date

from django.core.exceptions import FieldError
from django.db.models import QuerySet
from django_filters import rest_framework as rest_filters

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from comet.permissions import IsOwner
from events.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.api.serializers import ShortUserSerializer


class EventFilter(rest_filters.FilterSet):
    tags = rest_filters.CharFilter(method='filter_tags')
    name = rest_filters.CharFilter(field_name='name')
    author = rest_filters.CharFilter(field_name='author__username')
    city = rest_filters.CharFilter(field_name='city')
    country = rest_filters.CharFilter(field_name='country')
    date_start = rest_filters.DateFilter(field_name='date_expire', lookup_expr='gte')
    date_end = rest_filters.DateFilter(field_name='date_expire', lookup_expr='lte')
    following_in_events = rest_filters.BooleanFilter(method='filter_following')


    class Meta:
        model = Event
        fields = ['tags', 'name', 'author', 'date_start', 'date_end', 'city', 'country', 'following_in_events']

    def filter_tags(self, queryset, name, tags):
        return queryset.filter(tags__name__in=tags.split(','))

    # return all events of current user where his following go
    def filter_following(self, queryset, name, option):
        if option:
            user = self.request.user
            return Event.objects.filter(members__username__in=user.following.all().values('username'))
        else:
            return Event.objects.all()

class EventRegisterViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventRegisterSerializer
    http_method_names = ['post']

    def get_permissions(self):
        return (IsAuthenticated(),)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get', 'patch', 'delete']
    filter_backends = (filters.SearchFilter, rest_filters.DjangoFilterBackend, )
    search_fields = ('name', 'author__username', )
    filter_class = EventFilter


    def get_permissions(self):
        if self.request.method == 'PATCH' or self.request.method == 'PUT' or self.request.method == 'DELETE':
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

    @action(detail=True, methods=['get'])
    def is_follower (self, request):
        queryset = Event.objects.filter(date_expire__gt=date.today())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        params = request.GET.dict()
        try:

            result = Event.objects.filter(**params)
            return Response(ShortEventSerializer(result).data)

        except FieldError:
            return Response('invalid_params')

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

