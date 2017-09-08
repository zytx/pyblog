from django.db import models
import django.utils.timezone as timezone

# Create your models here.

class Image(models.Model):
    img = models.ImageField(upload_to=timezone.localdate().strftime('%Y/%m/%d'))
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