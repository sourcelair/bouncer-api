from django.db import models


class EntryBase(models.Model):
    """
    Abstract base class for the reason why an entry is blacklisted.
    """

    reason = models.TextField()

    class Meta:
        abstract = True


class IPEntry(EntryBase):
    """
    Model for IP entries in blacklist.
    """

    entry_value = models.GenericIPAddressField(unique=True)


class EmailEntry(EntryBase):
    """
    Model for email entries in blacklist.
    """

    entry_value = models.EmailField(unique=True)


class EmailHostEntry(EntryBase):
    """
    Model for email host entries in blacklist.
    """

    entry_value = models.CharField(max_length=254, unique=True)
