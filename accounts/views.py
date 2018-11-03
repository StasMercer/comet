from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.mail import send_mail
import random
from rest_framework.permissions import AllowAny
from .models import CustomUser


@api_view(['GET',])
@permission_classes((AllowAny, ))
def check_username(request, username=None):
    print(request.user)
    if username:
        user = CustomUser.objects.filter(username__iexact=username)
        if user:
            return Response('username is used')
    return Response('username is unique')


@api_view(['GET',])
@permission_classes((AllowAny, ))
def check_email(request, email=None):

    try:
        validate_email(email)
        valid_email = True
    except ValidationError:
        valid_email = False
    print(valid_email)
    if valid_email:
        user = CustomUser.objects.filter(email__iexact=email)
        if user:
            return Response('email is used')
    else:
        return Response('email not valid')

    return Response('email is unique')


@api_view()
@permission_classes((AllowAny, ))
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

        return Response({'detail': 'email sent to '+email, 'verification_code': str(rand_num)})

    else:
        return Response('email not valid')



