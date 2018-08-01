from django.db.models.signals import pre_save
from django.dispatch import receiver
from blacklist import models


@receiver(pre_save, sender=models.IPEntry)
@receiver(pre_save, sender=models.EmailEntry)
@receiver(pre_save, sender=models.EmailHostEntry)
def ip_entry_handler(instance, **kwargs):
    """
    Handler that assigns to lower_case_entry_value the entry_value.lower()
    """

    instance.lower_case_entry_value = instance.entry_value.lower()
