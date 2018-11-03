from django.urls import path, include
from rest_framework import routers
from events.api.viewsets import EventViewSet


router = routers.DefaultRouter()

router.register('', EventViewSet)

urlpatterns = [
    path('', include(router.urls))
]