from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save, post_delete
from django.dispatch.dispatcher import receiver
import time
import os


def img_path(instance, filename):
    return 'img/{0}/{1}{2}'.format(timezone.localdate().strftime('%Y/%m/%d'), int(round(time.time() * 1000)),
                                   os.path.splitext(filename)[1])


class Image(models.Model):
    img = models.ImageField(verbose_name='图片', upload_to=img_path)
    rel = models.ForeignKey('pyblog.Article', verbose_name='文章', blank=True, null=True)

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = '图片'

    def __str__(self):
        return self.img.name


@receiver(pre_save, sender=Image)
def img_update(sender, instance, **kwargs):
    """
    文件更新时删除旧文件
    """
    if instance.id:
        old = sender.objects.get(id=instance.id)
        old.img.delete(False)


@receiver(post_delete, sender=Image)
def img_delete(sender, instance, **kwargs):
    """
    文件随数据库删除
    """
    instance.img.delete(False)
