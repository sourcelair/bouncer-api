from django.contrib import admin
from blacklist import models


@admin.register(models.IPEntry, models.EmailHostEntry)
class EntryAdmin(admin.ModelAdmin):
    fields = ["entry_value", "lower_case_entry_value", "reason"]
    search_fields = ["entry_value"]


@admin.register(models.EmailEntry)
class EmailEntryAdmin(admin.ModelAdmin):
    fields = ["entry_value", "lower_case_entry_value", "hashed_value", "reason"]
    search_fields = ["entry_value", "hashed_value"]
    readonly_fields = ["hashed_value"]
