from django.contrib import admin
from authentication import models


@admin.register(models.AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    fields = ["user", "key"]
    search_fields = ["user", "key"]
    readonly_fields = ["key"]
