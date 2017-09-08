from django import forms
from django.utils.html import conditional_escape

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
from django.utils.safestring import mark_safe


class EditormdWidget(forms.Textarea):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        html = """
            <div id="editormd">
                <textarea name="%(name)s" style="display:none;">%(body)s</textarea>
            </div>
            <script type="text/javascript">
                $(function () {
                    var editor = editormd({
                        id: 'editormd',
                        path: '%(path)s',
                        height: 400,
                        emoji: true,
                        toolbarIcons : function() {
                            return ["undo", "redo", "|", "bold", "del", "italic", "quote", "hr", "|", "h2", "h3", "|", "list-ul", "list-ol", "|", "link", "reference-link", "code", "code-block", "|", "table", "datetime", "emoji", "html-entities", "image", "||", "watch", "preview", "fullscreen"]
                        },
                        imageUpload    : true,
                        imageFormats   : ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
                        imageUploadURL : "/editormd/upload/",
                        codeFold : true,

                    });
                    editormd.emoji = {
                        'path':'//assets-cdn.github.com/images/icons/emoji/',
                        'ext':'.png'
                    }
                    editormd.twemoji = {
                        path: "//cdn.bootcss.com/twemoji/2.5.0/2/svg/", 
                        ext: ".svg"
                    }
                });
                
                
            </script>
            """ % {
            'name': name,
            'path': '//cdn.jsdelivr.net/gh/pandao/editor.md@1.5.0/lib/',
            'body': conditional_escape(force_text(value)),
        }
        return mark_safe(html)

    class Media:
        css = {
            "all": ('//cdn.jsdelivr.net/gh/pandao/editor.md@1.5.0/css/editormd.min.css',)
        }
        js = (
            '//cdn.bootcss.com/jquery/3.2.1/jquery.min.js',
            '//cdn.jsdelivr.net/gh/pandao/editor.md@1.5.0/editormd.min.js',
        )
