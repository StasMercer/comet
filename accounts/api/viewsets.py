from rest_framework.response import Response
from rest_framework import viewsets
from accounts.models import CustomUser, Rate
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import action


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

    # heap of detail endpoints to make additional queries
    @action(detail=True, methods=['patch'])
    def add_following(self, request, username=None):
        user = self.get_object()
        following = CustomUser.objects.get(username=request.data.get('following_username'))
        user.following.add(following)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['patch'])
    def add_follower(self, request, username=None):
        user = self.get_object()
        follower = CustomUser.objects.get(username=request.data.get('follower_username'))
        user.followers.add(follower)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['patch'])
    def remove_following(self, request, username=None):
        user = self.get_object()
        following = CustomUser.objects.get(username=request.data.get('following_username'))
        user.following.remove(following)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['patch'])
    def remove_follower(self, request, username=None):
        user = self.get_object()
        follower = CustomUser.objects.get(username=request.data.get('follower_username'))
        user.followers.remove(follower)
        return Response({'status': 'ok'})


class RateViewsSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class UserPhotoViewsSet(viewsets.ModelViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = PhotoSerializer


