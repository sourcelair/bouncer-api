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

    entry_value = models.GenericIPAddressField()
    lower_case_entry_value = models.GenericIPAddressField(unique=True, editable=False)

    def __str__(self):
        return self.entry_value


class EmailEntry(EntryBase):
    """
    Model for email entries in blacklist.
    """

    entry_value = models.EmailField()
    lower_case_entry_value = models.EmailField(unique=True, editable=False)

    def __str__(self):
        return self.entry_value


class EmailHostEntry(EntryBase):
    """
    Model for email host entries in blacklist.
    """

    entry_value = models.CharField(max_length=254)
    lower_case_entry_value = models.CharField(
        max_length=254, unique=True, editable=False
    )

    def __str__(self):
        return self.entry_value
