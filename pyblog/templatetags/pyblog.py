import re

import mistune
from django import template
from django.conf import settings
from django.utils.html import mark_safe

from pyblog import models

register = template.Library()

outline_list = []


class Renderer(mistune.Renderer):

    def __init__(self):
        global outline_list
        outline_list = []
        self.h_pattern = re.compile(r'<([\w]+) [^>]+.*\1>')
        super(__class__, self).__init__()

    def block_code(self, code, lang):
        if lang:
            return '\n<pre class="prettyprint linenums lang-%s">%s</pre>\n' % (lang, mistune.escape(code))
        else:
            return '\n<pre class="prettyprint linenums">%s</pre>\n' % mistune.escape(code)

    def header(self, text, level, raw=None):
        """Rendering header/heading tags like ``<h1>`` ``<h2>``.

        :param text: rendered text content for the header.
        :param level: a number for the header level, for example: 1.
        :param raw: raw text content of the header.
        """
        if level == 2:
            clean_text = self.h_pattern.sub('', text)
            outline_list.append([clean_text, ])
            return '<h%d id="h-%d" class="h%d">%d. %s</h%d>\n' % (
                level, len(outline_list), level + 3, len(outline_list), text, level)
        elif level == 3:
            clean_text = self.h_pattern.sub('', text)
            if len(outline_list[-1]) >= 2:
                outline_list[-1][-1].append(clean_text)
            else:
                outline_list[-1].append([clean_text, ])
            return '<h%d id="h-%d-%d" class="h%d">%d.%d. %s</h%d>\n' % (
                level, len(outline_list), len(outline_list[-1][-1]), level + 3, len(outline_list), len(outline_list[-1][-1]), text, level)
        else:
            return '<h%d class="h%d">%s</h%d>\n' % (level, level + 3, text, level)

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

markdown_to_html = mistune.Markdown(escape=False, renderer=Renderer(), hard_wrap=True)  # hard_wrap:回车换行


@register.filter()
def denewline(text):
    return text.replace("\n", "")


@register.simple_tag
def hotArticle():
    return models.Post.objects.filter(is_published=True)[:8]


@register.simple_tag
def tags():
    return models.Tag.objects.filter(post__isnull=False).distinct().values('title')


@register.simple_tag
def outline():
    if len(outline_list) == 0:
        return ''
    result = '<h4 class="pb-2">目录</h4><ul class="nav nav-pills flex-column text-truncate">'
    for index_h2, item in enumerate(outline_list, 1):
        result += '<li><a class="nav-link" title="%s" href="#h-%d">%d. %s</a>' % (item[0], index_h2, index_h2, item[0])
        if len(item) >= 2:
            result += '<ul class="nav nav-pills flex-column ml-3 d-none">'
            for index_h3, text in enumerate(item[1], 1):
                result += '<li><a class="nav-link" title="%s" href="#h-%d-%d">%d.%d. %s</a></li>' % (
                    text, index_h2, index_h3, index_h2, index_h3, text)
            result += '</ul>'
        result += '</li>'
    result += '</ul>'
    return mark_safe(result)
