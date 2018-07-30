from django.urls import path

from . import views

app_name = "blacklist"

urlpatterns = [path("", views.IPRequestView.as_view(), name="ip-request")]
