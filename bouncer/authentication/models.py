import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from blacklist.models import EmailEntry
from django.utils.crypto import get_random_string


class AuthToken(models.Model):
    key = models.CharField(_("Key"), max_length=32, primary_key=True)
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="auth_token", verbose_name=_("User")
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("AuthToken")
        verbose_name_plural = _("AuthTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(AuthToken, self).save(*args, **kwargs)

    def generate_key(self):
        return get_random_string(length=32)

    def __str__(self):
        return self.key
