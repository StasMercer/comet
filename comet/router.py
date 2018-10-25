from accounts.api.viewsets import *
from accounts import views
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()
router.register('', UserViewSet)

