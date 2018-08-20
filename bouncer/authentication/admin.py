from django.contrib import admin
from authentication import models


@admin.register(models.AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    fields = ["user"]
    search_fields = ["user", "key"]
