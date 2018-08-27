from django.urls import path
from blacklist import views

app_name = "blacklist"

urlpatterns = [
    path("", views.GetRequestView.as_view(), name="get_request"),
    path("add/", views.PostRequestViewSet, name="post_request"),
]
