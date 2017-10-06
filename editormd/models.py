from django.db import models
from django.utils import timezone
from pyblog.models import Article

# Create your models here.

class Image(models.Model):
    img = models.ImageField(verbose_name = '图片', upload_to=timezone.localdate().strftime('%Y/%m/%d'))
    rel = models.ForeignKey(Article, verbose_name = '文章', blank=True, null=True)
    class Meta:
        verbose_name = '图片'
        verbose_name_plural = '图片'
    def __str__(self):
        return self.img.name

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

@receiver(pre_delete, sender=Image)
def mymodel_delete(sender, instance, **kwargs):
    '''
    文件随数据库删除
    '''
    # Pass false so FileField doesn't save the model.
    instance.img.delete(False)