from django.contrib import admin
from django.db import models
from editormd.models import Image
from django.core.files.storage import default_storage

# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display = ('preview', 'img', 'rel')
    readonly_fields = ('preview_full',)
    search_fields = ('img',)
    def preview(self,obj):
        return '<img src="%s/h150" />' %(obj.img.url)
    def preview_full(self,obj):
        return '<img src="%s" />' %(obj.img.url)
    preview.allow_tags = preview_full.allow_tags = True
    preview.short_description = preview_full.short_description = "预览"

admin.site.register(Image,ImageAdmin)