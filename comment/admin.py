from django.contrib import admin
from . import models
from django.shortcuts import reverse
from django.utils import safestring
from pyblog.models import Post


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'content', 'post_link', 'date', 'status')
    search_fields = ('user__nickname', 'user__email', 'nickname', 'email', 'content')

    class Media:
        css = {
            "all": (
                "comment/admin/emoji.css",
                "//cdn.jsdelivr.net/npm/emojionearea@3/dist/emojionearea.min.css"
            )
        }
        js = (
            "//cdn.jsdelivr.net/combine/npm/jquery@3,npm/emojione@3,npm/emojionearea@3",
            "comment/admin/emoji.js",
        )

    def username(self, obj):
        return obj.nickname if obj.nickname else obj.user.nickname

    username.short_description = '作者'

    def status(self, obj):
        return '-' if obj.nickname else '注册'

    status.short_description = '用户状态'

    def post_link(self, obj):
        post = Post.objects.get(uid=obj.post_uid)
        return safestring.mark_safe(
            f"<a href='{reverse('admin:pyblog_post_change', args=(post.id,))}'>{post.title}</a>")

    post_link.short_description = '文章'
