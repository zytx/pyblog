import json

from django import template
from django.utils.html import mark_safe

from pyblog import models

register = template.Library()


@register.filter()
def denewline(text):
    return text.replace("\n", "")


@register.simple_tag
def hotArticle():
    return models.Post.objects.filter(is_published=True)[:8]


@register.simple_tag
def tags():
    return models.Tag.objects.filter(post__isnull=False).distinct().values('title')


@register.filter()
def outline(text):
    try:
        outline_list = json.loads(text)
    except json.JSONDecodeError:
        return ''
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
