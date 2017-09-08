from django import template

register = template.Library()

import mistune

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
        return '<h%d class="h%d">%s</h%d>\n' % (level, level+2 ,text, level)

md = mistune.Markdown(escape=False,renderer=Renderer())

@register.filter()
def markdown(text):
    return md(text)