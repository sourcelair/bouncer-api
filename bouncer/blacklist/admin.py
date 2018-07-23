from django.contrib import admin
from blacklist import models

admin.site.register(models.IPEntry)
admin.site.register(models.EmailEntry)
admin.site.register(models.EmailHostEntry)
