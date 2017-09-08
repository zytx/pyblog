from django.contrib import admin
from django.db import models
from editormd.widget import EditormdWidget
from .models import Tag,Category,Article
from .forms import ArticleAdminForm
from django import forms

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


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title','type','pub_date','is_pub')
    search_fields = ('title',)
    date_hierarchy = ('pub_date')
    list_filter = ('category',)
    filter_horizontal = ('tags',)
    formfield_overrides = {
        models.TextField: {'widget': EditormdWidget()},
    }
    prepopulated_fields = {"slug": ("title",)}

