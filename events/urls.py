from django.urls import path, include
from rest_framework import routers
from events.api import viewsets


router = routers.DefaultRouter()

router.register('photos', viewsets.PhotoViewSet)
router.register('tags', viewsets.TagViewSet)
router.register('create', viewsets.EventRegisterViewSet)
router.register('', viewsets.EventViewSet)


urlpatterns = [

]

urlpatterns += router.urls

