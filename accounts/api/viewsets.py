from requests import Response
from rest_framework import viewsets
from accounts.models import CustomUser, Rate
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    """
        Return a list of all the existing users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserViewSet, self).get_permissions()


class RateViewsSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class UserPhotoViewsSet(viewsets.ModelViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = PhotoSerializer


