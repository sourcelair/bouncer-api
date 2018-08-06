from django.urls import path, include
from rest_framework import routers
from blacklist import views

app_name = "blacklist"

router = routers.DefaultRouter()
router.register("", views.RequestView, base_name="request")

urlpatterns = [path("", include(router.urls))]
