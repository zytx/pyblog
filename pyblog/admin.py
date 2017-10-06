from django.contrib import admin
from django.db import models
from .models import Tag,Category,Article
from .forms import ArticleAdminForm
from django import forms
from editormd.models import Image
from editormd.admin import ImageAdmin


admin.site.site_header = "Administration"
admin.site.site_title = "Mr.Z's Blog"
admin.site.empty_value_display = "--空--"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title","slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title","slug")
    prepopulated_fields = {"slug": ("title",)}


class ImageInline(admin.TabularInline):
    model = Image
    def preview(self,obj):
        return '<img src="%s" height="150" />' %(obj.img.url)
    readonly_fields = ('preview',)
    preview.allow_tags = True
    preview.short_description = "预览"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title','category','type','pub_date','mod_date','is_pub')
    search_fields = ('title',)
    date_hierarchy = ('pub_date')
    list_filter = ('category',)
    filter_horizontal = ('tags',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
            ImageInline,
        ]
