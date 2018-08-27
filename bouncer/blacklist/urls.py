from django.urls import path
from blacklist import views

app_name = "blacklist"

urlpatterns = [
    path("", views.GetRequestView.as_view(), name="get_request"),
    path(
        "add/",
        views.PostRequestViewSet.as_view({"post": "add_entry"}),
        name="post_request",
    ),
]
