from django.contrib import admin
from .models import Comment

# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('username','content','article','date','status')
    search_fields = ('user__nikename','user__email','nikename','email','content')

    class Media:
        css = {
            "all": ("comment/admin/emoji.css",
                "//cdn.jsdelivr.net/gh/mervick/emojionearea@3.1.8/dist/emojionearea.min.css"
            )
        }
        js = ("//cdn.bootcss.com/jquery/3.2.1/jquery.min.js",
            "//cdn.bootcss.com/emojione/2.2.7/lib/js/emojione.min.js",
            "//cdn.jsdelivr.net/gh/mervick/emojionearea@3.1.8/dist/emojionearea.min.js",
            "comment/admin/emoji.js",
        )

    def username(self, obj):
        return obj.nikename if obj.nikename else obj.user.nikename
    username.short_description = '作者'

    def status(self, obj):
        return '-' if obj.nikename else '注册'
    status.short_description = '用户状态'