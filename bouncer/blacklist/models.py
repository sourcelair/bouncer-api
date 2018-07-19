from django.db import models

# Create your models here.
class IPEntry(models.Model):
	entry_value = models.GenericIPAddressField()
	reason = models.TextField()

class EmailEntry(models.Model):
	entry_value = models.EmailField()
	reason = models.TextField()

class EmailHostEntry(models.Model):
	entry_value = models.CharField(max_length = 254)
	reason = models.TextField()