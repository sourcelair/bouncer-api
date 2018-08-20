from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from authentication import models


class Authentication(authentication.TokenAuthentication):
    def authenticate_credentials(self, key):
        model = models.AuthToken
        token = model.objects.select_related("user").get(key=key)

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        return (token.user, token)