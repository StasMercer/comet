from django.core.exceptions import ValidationError
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.mail import send_mail
from rest_framework.validators import UniqueValidator
from django.db import models
import random

from accounts.api.serializers import UserCheckSerializer
from .models import CustomUser
@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def check_user(request, username, email):


    if username:
        user = CustomUser.objects.filter(username__iexact=username)
        if user:
            return Response('username is used')

    if email:
        user = CustomUser.objects.filter(email__iexact=email)
        if user:
            return Response('email is used')

    return Response('all fields unique')


class UserCheckApiView(generics.ListCreateAPIView):
    serializer_class = UserCheckSerializer
    lookup_field = 'username'

    def post(self, request, format=None):
        print(request)
        return Response("ok")

    def get_queryset(self):
        return CustomUser.objects.all()

@api_view()
def verify_email(request, email):


    try:
        validate_email(email)
        valid_email = True
    except ValidationError:
        valid_email = False

    if valid_email:

        rand_num = random.randint(1000, 10000)

        send_mail(
            'Commet confirmation code',
            'Hey budy, please confirm your email with code you see bellow\n'+
            str(rand_num),
            'pro100.stas.ru@gmail.com',
            [email],
            fail_silently=False,
        )

        return Response({'detail': 'email sent to '+email, 'verification_code:': str(rand_num)})

    else:
        return Response('email not valid')



