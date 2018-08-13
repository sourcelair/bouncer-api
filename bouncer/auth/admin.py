from django.contrib import admin
from auth import models


@admin.register(models.UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    fields = ["user", "key"]
    search_fields = ["user", "key"]
    readonly_fields = ["key"]
