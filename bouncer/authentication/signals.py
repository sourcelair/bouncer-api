from django.db.models.signals import pre_save
from django.dispatch import receiver
from authentication import models


@receiver(pre_save, sender=models.UserToken)
def email_entry_handler(sender, instance, **kwargs):
    """
    Handler that assigns to key a random string
    """

    key = generate_key()
