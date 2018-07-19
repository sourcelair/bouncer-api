from django.db import models

# Create your models here.
class IP_Entry(models.Model):
	entry_value = models.GenericIPAddressField()

class Email_Entry(models.Model):
	entry_value = models.EmailField()

class Host_Entry(models.Model):
	entry_value = models.CharField(max_length = 254)