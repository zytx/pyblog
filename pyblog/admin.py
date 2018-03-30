from django.contrib import admin
from django.utils.safestring import mark_safe

from editormd.admin import ImageAdmin
from comment.admin import CommentAdmin
from .forms import ArticleAdminForm
from .models import Tag, Category, Article, Comment, Image

admin.site.site_header = "Administration"
admin.site.site_title = "Mr.Z's Blog"
admin.site.empty_value_display = "--空--"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


class ImageInline(admin.TabularInline):
    model = Image
    readonly_fields = ('preview',)

    def preview(self, obj):
        return mark_safe('<img src="%s/h150" />' % obj.img.url)

    preview.short_description = "预览"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'category', 'type', 'pub_date', 'mod_date', 'is_pub')
    readonly_fields = ('author_info',)
    search_fields = ('title',)
    date_hierarchy = 'pub_date'
    list_filter = ('category',)
    list_editable = ('category', 'type')
    filter_horizontal = ('tags',)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ImageInline,
    ]

    def save_model(self, request, obj, form, change):
        """
        保存文章时自动添加作者
        """
        obj.author = request.user
        super(ArticleAdmin, self).save_model(request, obj, form, change)

    def author_info(self, obj):
        return mark_safe('昵称: %s<br/>邮箱: %s' % (obj.author.nickname, obj.author.email))

    author_info.short_description = '作者'


admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)
