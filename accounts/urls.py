from django.urls import path, include
from . import views
from allauth.account.views import ConfirmEmailView
from django.views.generic import TemplateView


urlpatterns = [
    path('registration/account-email-verification-sent/', views.null_view , name='account_email_verification_sent'),

    path('registration/account-confirm-email/<str:key>/',
         TemplateView.as_view(template_name='accounts/index.html'),
         name='account_confirm_email'),

    path('password-reset/confirm/(<str:uidb64>)/(<str:token>)/',
         views.null_view,
         name='password_reset_confirm'),

    # Default urls
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls'))
]

