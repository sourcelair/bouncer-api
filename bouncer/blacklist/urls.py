from django.urls import path
from blacklist import views

app_name = "blacklist"

urlpatterns = [path("", views.BlacklistView.as_view(), name="blacklist_request")]
