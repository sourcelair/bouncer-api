from django.urls import path
from blacklist import views

app_name = "blacklist"

urlpatterns = [path("", views.RequestView.as_view(), name="request")]
