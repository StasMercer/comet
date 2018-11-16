from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.validators import validate_email
from django.core.mail import send_mail
import random
from rest_framework.permissions import AllowAny
from .models import CustomUser, UserPhoto, Rate
from events.models import Event
from rest_framework.views import APIView
from .api import serializers
from django.shortcuts import get_object_or_404

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


class UserDetail(APIView):
    def get(self, request, username):
        user = get_object_or_404(CustomUser, username=username)
        is_current = False
        if request.user == user:
            is_current = True

        friends = [
            {'username': friend.username, 'avatar': friend.avatar.url}
            for friend in user.friends.iterator()
        ]

        photos = [
            {'id': photo.id, 'url': photo.img_value.url}
            for photo in UserPhoto.objects.filter(photo_user__username=username)
        ]

        tags = [tag.username for tag in user.tags.iterator()]

        events_created = [
            {'id': event.id, 'name': event.name, }
            for event in Event.objects.filter(author__username=username)
        ]

        rate = [rate.value for rate in Rate.objects.filter(to_user__username=username)]
        if len(rate) != 0:
            rate = float(sum(rate)/len(rate))

        events_visited = [
            {'id': event.id,'name': event.name}
            for event in Event.objects.filter(members__username=username)
        ]

        data = {
                'is_current': is_current,
                'username': user.username,
                'avatar': user.avatar.url,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth,
                'phone_number': user.phone_number,
                'friends': friends,
                'photos': photos,
                'tags': tags,
                'events_created': events_created,
                'rate': rate,
                'events_visited': events_visited,
                }

        return Response(data)
