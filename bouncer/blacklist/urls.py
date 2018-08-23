from django.urls import path
from blacklist import views

app_name = "blacklist"

urlpatterns = [path("", views.GetRequestView.as_view(), name="request")]
