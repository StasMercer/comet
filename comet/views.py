from PIL import Image
from django.shortcuts import HttpResponse, render
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from accounts.models import CustomUser


class UserState(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return Response(str(request.user.username) + '  ' + str(request.user.auth_token.key))
        else:
            return Response('user is not logged in, or authenticated')






def show_img(request, folder, img_name):

    img_path = settings.MEDIA_ROOT + '\\'+folder+'\\' + img_name

    try:
        with open(img_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        return HttpResponse('file open error')

