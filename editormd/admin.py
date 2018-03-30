from django.contrib import admin
from editormd.models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ('preview', 'img', 'rel')
    readonly_fields = ('preview_full',)
    search_fields = ('img',)

    def preview(self, obj):
        print(obj.img.size)
        return '<img src="%s/h150" />' % obj.img.url

    def preview_full(self, obj):
        return '<img src="%s" />' % obj.img.url

    preview.allow_tags = preview_full.allow_tags = True
    preview.short_description = preview_full.short_description = "预览"


admin.site.register(Image, ImageAdmin)
