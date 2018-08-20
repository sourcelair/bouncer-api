from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from authentication import models


class TokenAuthentication(authentication.TokenAuthentication):
    def authenticate_credentials(self, key):
        self.model = models.AuthToken
        return super(Authentication, self).authenticate_credentials(key)
