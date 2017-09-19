from django.db import models
from django.conf import settings

# Create your models here.


class Tag(models.Model):
    title = models.CharField('标签', max_length=100, unique=True)
    slug = models.SlugField('别名(URL)', max_length=100, unique=True)
    keywords = models.CharField('关键字', blank=True, null=True, max_length = 200, help_text=('用于Keywords标签，逗号隔开'))
    desc = models.CharField('描述', blank=True, null=True, max_length = 500)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签' 
    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField('分类', max_length = 100, unique=True)
    slug = models.SlugField('别名(URL)', max_length=100, unique=True)
    keywords = models.CharField('关键字（自动追加Tag）', blank=True, null=True, max_length = 200, help_text=('用于Keywords标签，逗号隔开'))
    desc = models.CharField('描述', blank=True, null=True, max_length = 500)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类' 

    def __str__(self):
        return self.title


class Article(models.Model):
    is_pub = models.BooleanField('发布', default=True)
    title = models.CharField('标题', max_length=100, unique=True)
    slug = models.SlugField('别名(URL)', max_length = 100, unique=True)
    content = models.TextField('正文')
    #content_html = models.TextField('HTML正文(由content生成，不要修改)')   #空间换时间。。
    keywords = models.CharField('关键字', blank=True, null=True, max_length=200, help_text=('用于Keywords标签，自动追加该文章Tag，逗号隔开'))
    desc = models.CharField('摘要', blank=True, null=True, max_length=500)
    TYPE_CHOICES = (
        (0, '文章'),
        (1, '页面'),
    )
    type = models.PositiveSmallIntegerField('文章类型', choices=TYPE_CHOICES,default=0)
    category = models.ForeignKey(Category, verbose_name = '分类')
    tags = models.ManyToManyField(Tag, verbose_name = '标签')
    pub_date = models.DateTimeField('创建日期', auto_now_add=True)
    mod_date = models.DateTimeField('修改日期', auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='作者')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title