from django import template

register = template.Library()


@register.filter()
def avatar(email, size=60):
    import hashlib
    if email:
        return "//cdn.v2ex.com/gravatar/%s.jpg?s=%s&d=retro" % (hashlib.md5(str(email).encode('utf-8')).hexdigest(),
                                                                size)
    else:
        return '//cdn.v2ex.com/gravatar/?s=%s&d=mm' % size
