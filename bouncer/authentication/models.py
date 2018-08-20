from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string


class AuthToken(models.Model):
    def generate_key():
        return get_random_string(length=32)

    key = models.CharField(
        _("Key"), max_length=32, default=generate_key, primary_key=True, editable=False
    )
    user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="auth_token", verbose_name=_("User")
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        verbose_name = _("AuthToken")
        verbose_name_plural = _("AuthTokens")

    def __str__(self):
        return self.key
