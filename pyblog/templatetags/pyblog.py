from django import template
from django.conf import settings
from django.utils.html import mark_safe
import mistune
import re
from pyblog.models import Article,Category,Tag
from django.db.models import Count

register = template.Library()

outline = []

class Renderer(mistune.Renderer):

    def __init__(self):
        global outline
        outline=[]
        self.h_counter=0
        self.h_pattern = re.compile(r'<([\w]+) [^>]+.*\1>')
        super(__class__,self).__init__()

    def block_code(self, code, lang):
        if lang:
            return '\n<pre class="prettyprint linenums lang-%s">%s</pre>\n' % (lang,mistune.escape(code))
        else:
            return '\n<pre class="prettyprint linenums">%s</pre>\n' % mistune.escape(code)

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        clean = self.h_pattern.sub('',text)
        if level==2:
            outline.append(clean)
            self.h_last=2
            self.h_counter+=1
        elif level==3:
            if self.h_last==3:
                outline[-1].append(clean)
            else:
                outline.append([clean,])
            self.h_last=3
            self.h_counter+=1
        if level in (2,3):
            return '<h%d id="h-%d" class="h%d">%s</h%d>\n' % (level, self.h_counter, level+3, text, level)
        else:
            return '<h%d class="h%d">%s</h%d>\n' % (level, level+3, text, level)

    def autolink(self, link, is_email=False):
        """Rendering a given link or email address.

        :param link: link content or email address.
        :param is_email: whether this is an email or not.
        """
        text = link = mistune.escape(link)

        if is_email:
            link = 'mailto:%s' % link
        if settings.DOMAIN_NAME in link:
            return '<a href="%s">%s</a>' % (link, text)
        else:
            return '<a href="%s" rel="external nofollow" target="_blank">%s</a>' % (link, text)

    def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        link = mistune.escape_link(link)
        if settings.DOMAIN_NAME in link:
            if not title:
                return '<a href="%s">%s</a>' % (link, text)
            title = mistune.escape(title, quote=True)
            return '<a href="%s" title="%s">%s</a>' % (link, title, text)
        else:
            if not title:
                return '<a href="%s" rel="external nofollow" target="_blank">%s</a>' % (link, text)
            title = mistune.escape(title, quote=True)
            return '<a href="%s" title="%s" rel="external nofollow" target="_blank">%s</a>' % (link, title, text)

    def table(self, header, body):
        """Rendering table element. Wrap header and body in it.

        :param header: header part of the table.
        :param body: body part of the table.
        """
        return (
            '<table class="table table-bordered table-hover table-sm">\n<thead>%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (header, body)

@register.filter()
def markdown(text):
    md = mistune.Markdown(escape=False,renderer=Renderer(),hard_wrap=True) #hard_wrap:回车换行
    return md(text)


@register.filter()
def denewline(text):
    return text.replace("\n","")

@register.simple_tag
def hotArticle():
    return Article.objects.filter(is_pub=True).annotate(Count('comment')).order_by('-comment__count','-pub_date').values('title','slug','comment__count')[:8]


@register.simple_tag
def categorys():
    return Category.objects.values('title','slug')


@register.simple_tag
def tags():
    return Tag.objects.values('title','slug')


@register.simple_tag
def outline():
    if len(outline) == 0 : 
        return ''
    result='<h4 class="pb-2">目录</h4><ul class="nav nav-pills flex-column text-truncate">'
    counter = 0
    for item in outline:
        if isinstance(item,list):
            result+='<ul class="nav nav-pills flex-column ml-3">'
            for i in item:
                counter+=1
                result+='<li><a class="nav-link" href="#h-%d">%s</a></li>' % (counter,i)
            result+='</ul>'
        else:
            counter+=1
            result+='<li><a class="nav-link" href="#h-%d">%s</a></li>' % (counter,item)
    result+='</ul>'
    return mark_safe(result)
