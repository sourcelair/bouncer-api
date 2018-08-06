from django.urls import path, include
from rest_framework import routers
from blacklist import views

app_name = "blacklist"

urlpatterns = [path("", views.RequestView.as_view(), name="request")]
