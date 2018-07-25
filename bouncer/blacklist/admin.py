from django.contrib import admin
from blacklist import models


@admin.register(models.IPEntry, models.EmailEntry, models.EmailHostEntry)
class EntryAdmin(admin.ModelAdmin):
    fields = ["entry_value", "reason"]
    search_fields = ["lower_case_entry_value", "entry_value"]
