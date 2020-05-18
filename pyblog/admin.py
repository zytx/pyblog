from django.contrib import admin

from .forms import PostAdminForm
from .models import Tag, Post

admin.site.site_header = "Administration"
admin.site.site_title = "Mr.Z's Blog"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_count')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'type', 'tags_str', 'created_time', 'updated_time', 'is_published')
    search_fields = ('title',)
    date_hierarchy = 'created_time'
    list_filter = ('type', 'tags')
    filter_horizontal = ('tags',)
    prepopulated_fields = {"slug": ("title",)}
    fields = ('is_published', 'title', 'slug', 'content', 'type', 'tags', 'created_time', 'updated_time')
