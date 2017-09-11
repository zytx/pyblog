from django import template
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


@register.filter()
def markdown(text):
    md = mistune.Markdown(escape=False,renderer=Renderer())
    return md(text)


@register.filter()
def denewline(text):
    return text.replace("\n","")
