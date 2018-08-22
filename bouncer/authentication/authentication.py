from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from authentication import models


class TokenAuthentication(authentication.TokenAuthentication):
    model = models.AuthToken
