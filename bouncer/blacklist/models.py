from django.db import models


class EntryReason(models.Model):
    """Abstract base class for the reason why an entry is blacklisted."""

    reason = models.TextField()

    class Meta:
        abstract = True


# Create your models here.
class IPEntry(EntryReason):
    """Model for IP entries in blacklist."""

    entry_value = models.GenericIPAddressField()


class EmailEntry(EntryReason):
    """Model for email entries in blacklist."""

    entry_value = models.EmailField()


class EmailHostEntry(EntryReason):
    """Model for email host entries in blacklist."""

    entry_value = models.CharField(max_length=254)
