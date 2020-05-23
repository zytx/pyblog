from django.contrib import admin
from . import models


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'source_url', 'created_time')
    search_fields = ('title', 'tags__title')
