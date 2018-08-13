import binascii
import os

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class UserToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="auth_token", verbose_name=_("User")
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("UserToken")
        verbose_name_plural = _("UserTokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(UserToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
