from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST', ])
def frontend(request, key):
    return Response('email authentificated: ' + key)
