from django.contrib import admin
from .models import Comment

# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','nikename','content','article','date')
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
