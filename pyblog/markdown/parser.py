import json
import re

import mistune
from django.conf import settings
from mistune.scanner import escape, escape_html

from pyblog.markdown.plugins import plugin_table, plugin_footnotes


class PyBlogRenderer(mistune.HTMLRenderer):

    def __init__(self, **kwargs):
        self.h2_count = 0
        self.h2_last_count = 1
        self.h3_count = 0
        self.outline = []
        self.h_pattern = re.compile(r'<([\w]+) [^>]+.*\1>')
        super(PyBlogRenderer, self).__init__(**kwargs)

    def heading(self, text, level):
        if level == 2 and level != self.h2_last_count:
            self.h3_count = 0
        if level in (2, 3):
            setattr(self, f'h{level}_count', getattr(self, f'h{level}_count') + 1)

        if level == 2:
            clean_text = self.h_pattern.sub('', text)
            self.h2_last_count = self.h2_count
            self.outline.append([clean_text, ])
            return f'<h{level} id="h-{self.h2_count}" class="h{level + 3}">{self.h2_count}. {text}</h{level}>\n'
        elif level == 3:
            clean_text = self.h_pattern.sub('', text)
            if len(self.outline[-1]) >= 2:
                self.outline[-1][-1].append(clean_text)
            else:
                self.outline[-1].append([clean_text, ])
            return f'<h{level} id="h-{self.h2_count}-{self.h3_count}" class="h{level + 3}">' \
                   f'{self.h2_count}.{self.h3_count}. {text}</h{level}>\n'
        return f'<h{level} class="h{level + 3}">{text}</h{level}>\n'

    def block_code(self, code, info=None):
        html = '<pre class="prettyprint linenums'
        if info is not None:
            info = info.strip()
        if info:
            lang = info.split(None, 1)[0]
            lang = escape_html(lang)
            html += ' language-' + lang
        return html + '">' + escape(code) + '</pre>\n'

    def link(self, link, text=None, title=None):
        if text is None:
            text = link

        s = '<a href="' + self._safe_url(link) + '"'
        if title:
            s += ' title="' + escape_html(title) + '"'
        if settings.DOMAIN_NAME not in link:
            s += 'rel="external nofollow" target="_blank"'
        return s + '>' + (text or link) + '</a>'


markdown = mistune.create_markdown(renderer=PyBlogRenderer(),
                                   plugins=['url', 'strikethrough', plugin_table, plugin_footnotes])


def parse_markdown(text):
    html = markdown(text)
    outline = json.dumps(markdown.renderer.outline)
    markdown.renderer.outline.clear()
    markdown.renderer.h2_count = 0
    markdown.renderer.h2_last_count = 1
    markdown.renderer.h3_count = 0
    return html, outline
