from django.contrib import admin

from .forms import PostAdminForm
from .models import Tag, Post

admin.site.site_header = "Administration"
admin.site.site_title = "Mr.Z's Blog"
admin.site.empty_value_display = "--空--"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'type', 'created_time', 'updated_time', 'is_published')
    search_fields = ('title',)
    date_hierarchy = 'created_time'
    list_editable = ('type',)
    filter_horizontal = ('tags',)
    prepopulated_fields = {"slug": ("title",)}
    fields = ('is_published', 'title', 'slug', 'content', 'type', 'tags', 'created_time', 'updated_time')
