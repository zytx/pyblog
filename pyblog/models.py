import uuid

from django.db import models
from django.utils import timezone

from .templatetags.pyblog import markdown_to_html


class Tag(models.Model):
    uid = models.UUIDField('UID', default=uuid.uuid4)
    title = models.CharField('标题', max_length=100, unique=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def post_count(self):
        return self.post_set.count()

    post_count.short_description = '文章数'


class Post(models.Model):
    TYPE_Post = 0
    TYPE_PAGE = 1
    TYPE_CHOICES = (
        (TYPE_Post, '文章'),
        (TYPE_PAGE, '页面'),
    )
    uid = models.UUIDField('UID', default=uuid.uuid4)
    is_published = models.BooleanField('已发布', default=True)
    title = models.CharField('标题', max_length=100)
    slug = models.SlugField('别名(URL)', max_length=100, unique=True)
    content = models.TextField('正文 Markdown')
    content_html = models.TextField('正文 HTML', editable=False)
    type = models.PositiveSmallIntegerField('文章类型', choices=TYPE_CHOICES, default=TYPE_Post)
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    created_time = models.DateTimeField('创建日期', default=timezone.now)
    updated_time = models.DateTimeField('修改日期', default=timezone.now)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def tags_str(self, split=','):
        return split.join(self.tags.values_list('title', flat=True))

    tags_str.short_description = '标签'

    def save(self, *args, **kwargs):
        self.content_html = markdown_to_html(self.content)
        super(Post, self).save(*args, **kwargs)
