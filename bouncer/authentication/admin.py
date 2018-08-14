from django.contrib import admin
from authentication import models


@admin.register(models.UserToken)
class AuthTokenAdmin(admin.ModelAdmin):
    fields = ["user", "key", "permissions"]
    search_fields = ["user", "key"]
    readonly_fields = ["key"]
