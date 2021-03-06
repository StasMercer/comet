from rest_framework.response import Response
from rest_framework import viewsets
from accounts.models import CustomUser, Rate
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from comet.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django_filters import rest_framework as rest_filters


class UserRegisterViewSet(viewsets.ModelViewSet):
    """
        Return a list of all the existing users .
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = 'username'
    http_method_names = ['post', 'head', 'patch']

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserRegisterViewSet, self).get_permissions()


class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ['get', 'patch']
    filter_backends = (filters.SearchFilter, rest_filters.DjangoFilterBackend,)
    search_fields = ('username', 'first_name', 'last_name')
    filter_fields = ('country', 'city', 'date_of_birth')
    # heap of detail endpoints to make additional queries

    @action(detail=True, methods=['get'])
    def get_followers(self, request, username=None):
        user = self.get_object()
        serializer = ShortUserSerializer(user.followers.all(), many=True, read_only=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def is_follower(self, request, username=None):
        user = get_object_or_404(CustomUser, username=username)
        follower_username = request.GET.get('follower_username')
        qs = user.followers.filter(username__iexact=follower_username)
        if qs:
            return Response('follower')
        else:
            return Response('not follower')

    @action(detail=True, methods=['get'])
    def get_following(self, request, username=None):
        user = self.get_object()
        serializer = ShortUserSerializer(user.following.all(), many=True, read_only=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[IsOwner])
    def add_following(self, request, username=None):
        user = self.get_object()
        following = CustomUser.objects.get(username=request.data.get('following_username'))
        user.following.add(following)
        following.followers.add(user)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['patch'])
    def remove_following(self, request, username=None):
        user = self.get_object()
        following = CustomUser.objects.get(username=request.data.get('following_username'))
        user.following.remove(following)
        following.followers.remove(user)
        return Response({'status': 'ok'})


    @action(detail=True, methods=['patch'])
    def update_tags(self, request, username=None):

        user = self.get_object()
        user.tags.clear()

        for name in request.data.get('tags'):
            tag = Tag.objects.get(name__iexact=name)
            user.tags.add(tag)
        return Response(UserSerializer(user).data)


class RateViewsSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class UserPhotoViewsSet(viewsets.ModelViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = PhotoSerializer


