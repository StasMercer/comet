from accounts.api.viewsets import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('registration', UserViewSet)
router.register('', UserViewSet)