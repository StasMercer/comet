from django.urls import path, include
from . import views
from allauth.account.views import ConfirmEmailView
from django.views.generic import TemplateView
from rest_framework import routers
from accounts.api import viewsets
from rest_framework.authtoken import views as rest_views

router = routers.DefaultRouter()

router.register('users', viewsets.UserViewSet)
router.register('rate', viewsets.RateViewsSet)
router.register('photos', viewsets.UserPhotoViewsSet)

urlpatterns = [

    path('', include(router.urls)),
    path('user_detail/<str:username>/', views.UserDetail.as_view(), name = 'user_detail'),
    path('login/', rest_views.obtain_auth_token, name='login'),
    path('check_username/<str:username>/', views.check_username),
    path('check_email/<str:email>/', views.check_email),
    path('verify_email/<str:email>/', views.verify_email),

]