"""URL's for the chat app."""

from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ChatSessionView.as_view()),
    path('<uri>/', views.ChatSessionView.as_view()),
    path('<uri>/messages/', views.ChatSessionMessageView.as_view()),
]