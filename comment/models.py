from django.db import models
from django.conf import settings
from pyblog.models import Article
from django.core.mail import send_mail
from collections import OrderedDict

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='用户',null=True, blank=True)

    nikename = models.CharField('昵称',null=True, blank=True,max_length=30)
    email = models.EmailField('邮箱',null=True, blank=True)
    url = models.URLField('网站',null=True, blank=True)

    allow_email = models.BooleanField('有回复时通过邮件通知',default=True)
    is_pub = models.BooleanField('发布',default=True)
    article = models.ForeignKey(Article,verbose_name = '文章')
    content = models.TextField('评论')
    date = models.DateTimeField('创建日期',auto_now_add=True)

    parent = models.ForeignKey('self',null=True, blank=True)
    at = models.ForeignKey('self',null=True, blank=True,related_name="reply")

    ip = models.GenericIPAddressField('评论者IP', null=True, blank=True)
    ua = models.CharField('UA',null=True, blank=True,max_length=200)


    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论' 

    def __str__(self):
        return self.content[:30]

    def get_nikename(self):
        return self.nikename if self.nikename else self.user.nikename

    def get_email(self):
        return self.email if self.email else self.user.email

    def get_url(self):
        return self.url if self.url else self.user.url if self.user else None

    @staticmethod
    def get_comment_list(article):
        q = Comment.objects.select_related('user','parent','at__user').order_by('parent','date').filter(article=article,is_pub=True).defer('allow_email','article','is_pub','ip','ua')
        comments = OrderedDict()
        for comment in q:
            if comment.parent == None:
                comments[comment.id] = {
                    'parent': comment,
                    'reply' : []
                }
            else:
                comments[comment.parent.id]['reply'].append(comment)
        return comments

    def send_email(self,recipient_list):
        send_mail(
            "您在Mr.Z's Blog 的评论有了新回复",
            '%s 说：%s' % (self.get_nikename(),self.content),
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )