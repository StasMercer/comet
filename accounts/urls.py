from django.urls import path, include
from . import views
from allauth.account.views import ConfirmEmailView
from django.views.generic import TemplateView
from rest_framework import routers
from accounts.api import viewsets


router = routers.DefaultRouter()

router.register('registration', viewsets.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
    path('check_username/<str:username>/', views.check_username),
    path('check_email/<str:email>/', views.check_email),
    path('verify_email/<str:email>/', views.verify_email),

]
