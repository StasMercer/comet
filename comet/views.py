from django.shortcuts import HttpResponse, render
from rest_framework.decorators import api_view
from rest_framework.response import Response


def frontend(request):
    return render(request, 'frontend/signup/index.html')

