from django.db.models.signals import pre_save
from django.dispatch import receiver
from blacklist import models
from hashlib import sha256


@receiver(pre_save, sender=models.IPEntry)
def ip_entry_handler(sender, instance, **kwargs):
    """
    Handler that assigns to lower_case_entry_value the entry_value.lower()
    """

    instance.lower_case_entry_value = instance.entry_value.lower()


@receiver(pre_save, sender=models.EmailEntry)
def email_entry_handler(sender, instance, **kwargs):
    """
    Handler that assigns to lower_case_entry_value the entry_value.lower()
    """

    instance.lower_case_entry_value = instance.entry_value.lower()
    email_hasher = sha256(instance.lower_case_entry_value.encode())
    instance.hashed_value = email_hasher.hexdigest().lower()


@receiver(pre_save, sender=models.EmailHostEntry)
def email_host_entry_handler(sender, instance, **kwargs):
    """
    Handler that assigns to lower_case_entry_value the entry_value.lower()
    """

    instance.lower_case_entry_value = instance.entry_value.lower()
