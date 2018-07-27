from django.urls import path

from . import views

app_name = "blacklist"
urlpatterns = [
    path("", views.index, name="index"),
    path("?ip=<str:ip>", views.ip_request, name="ip request"),
]
