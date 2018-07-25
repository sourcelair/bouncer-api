from django.db.models.signals import pre_save
from django.dispatch import receiver
from blacklist import models


@receiver(pre_save, sender=models.IPEntry)
def ip_entry_handler(sender, instance, **kwargs):
    """
    Handler that assigns to lower_case_entry_value the entry_value.lower()
    """
    instance.lower_case_entry_value = instance.entry_value.lower()


@receiver(pre_save, sender=models.EmailEntry)
def ip_entry_handler(sender, instance, **kwargs):
    """
    Handler that assigns to lower_case_entry_value the entry_value.lower()
    """

    instance.lower_case_entry_value = instance.entry_value.lower()


@receiver(pre_save, sender=models.EmailHostEntry)
def ip_entry_handler(sender, instance, **kwargs):
    """
    Handler that assigns to lower_case_entry_value the entry_value.lower()
    """

    instance.lower_case_entry_value = instance.entry_value.lower()
