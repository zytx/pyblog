from django.db import models
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from collections import OrderedDict
import threading


class Comment(models.Model):
    """
    嵌套评论模型
    匿名/登录
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户', null=True, blank=True)

    nickname = models.CharField('昵称', null=True, blank=True, max_length=30)
    email = models.EmailField('邮箱', null=True, blank=True)
    url = models.URLField('网站', null=True, blank=True)

    allow_email = models.BooleanField('有回复时通过邮件通知', default=True)
    is_pub = models.BooleanField('发布', default=True)
    article = models.ForeignKey('pyblog.Article', verbose_name='文章')
    content = models.TextField('评论')
    date = models.DateTimeField('创建日期', auto_now_add=True)

    parent = models.ForeignKey('self', null=True, blank=True)
    at = models.ForeignKey('self', null=True, blank=True, related_name="reply")

    ip = models.GenericIPAddressField('评论者IP', null=True, blank=True)
    ua = models.CharField('UA', null=True, blank=True, max_length=200)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return self.content[:30]

    def get_nickname(self):
        """
        获取评论者昵称
        """
        return self.nickname if self.nickname else self.user.nickname

    def get_email(self):
        """
        获取评论者邮箱
        """
        return self.email if self.email else self.user.email

    def get_url(self):
        """
        获取评论者URL
        """
        return self.url if self.url else self.user.url if self.user else None

    @staticmethod
    def get_comment_list(article):
        """
        获取评论列表

        :param article: 外键文章
        """
        q = Comment.objects.select_related('user', 'parent', 'at__user').order_by('parent', 'date').filter(
            article=article, is_pub=True).defer('allow_email', 'article', 'is_pub', 'ip', 'ua')
        comments = OrderedDict()
        for comment in q:
            if comment.parent is None:
                comments[comment.id] = {
                    'parent': comment,
                    'reply': []
                }
            else:
                comments[comment.parent.id]['reply'].append(comment)
        return comments

    def send_email(self, to, path):
        """
        邮件通知，多线程异步发送
        通过模板加载HTML正文

        :param to: 发送到地址列表
        """
        subject = '您在' + settings.SITE_TITLE + '的评论有了新回复'
        content = loader.render_to_string(  # 渲染html模板
            '../templates/email.html',
            {
                'from_user': self.get_nickname(),
                'content': self.content,
                'back_url': 'http://%s%s' % (settings.EMAIL_BACK_DOMAIN, path),
            }
        )
        from_email = settings.DEFAULT_FROM_EMAIL

        def send(*args, **kwargs):
            msg = EmailMultiAlternatives(*args, **kwargs)
            msg.content_subtype = "html"
            msg.send()

        threading.Thread(target=send, args=(subject, content, from_email, to)).start()
