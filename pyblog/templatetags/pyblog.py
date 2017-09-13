from django import template
from django.conf import settings
import mistune

register = template.Library()


class Renderer(mistune.Renderer):

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
        return '<h%d class="h%d my-4">%s</h%d>\n' % (level, level+2 ,text, level)

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


@register.filter()
def markdown(text):
    md = mistune.Markdown(escape=False,renderer=Renderer())
    return md(text)


@register.filter()
def denewline(text):
    return text.replace("\n","")
