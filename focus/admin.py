from django.contrib import admin
from .models import DurationCategory

@admin.register(DurationCategory)
class DurationCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "minutes", "type", "is_active")
    search_fields = ("id", "minutes",)
