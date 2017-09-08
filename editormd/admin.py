from django.contrib import admin
from django.db import models
from editormd.models import Image

# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display = ("preview",)
    search_fields = ('name',)
    def preview(self,obj):
        return '<img src="/media/%s" height="100" width="100" />' %(obj.img)
    preview.allow_tags = True
    preview.short_description = "picture"

admin.site.register(Image,ImageAdmin)