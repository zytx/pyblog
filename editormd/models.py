from django.db import models
from django.utils import timezone
from pyblog.models import Article
from django.db.models.signals import pre_save,pre_delete
from django.dispatch.dispatcher import receiver

# Create your models here.

class Image(models.Model):
    img = models.ImageField(verbose_name = '图片', upload_to=timezone.localdate().strftime('%Y/%m/%d'))
    rel = models.ForeignKey(Article, verbose_name = '文章', blank=True, null=True)

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = '图片'

    def __str__(self):
        return self.img.name


@receiver(pre_save, sender=Image)
def mymodel_update(sender, instance, **kwargs):
    '''
    文件更新时删除旧文件
    '''
    if instance.id:
        old = sender.objects.get(id=instance.id)
        old.img.delete(False)


@receiver(pre_delete, sender=Image)
def mymodel_delete(sender, instance, **kwargs):
    '''
    文件随数据库删除
    '''
    instance.img.delete(False)