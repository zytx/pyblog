# Generated by Django 3.0 on 2020-05-23 22:59

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, verbose_name='UID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='标题')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, verbose_name='UID')),
                ('is_published', models.BooleanField(default=True, verbose_name='已发布')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='别名(URL)')),
                ('content', models.TextField(verbose_name='正文 Markdown')),
                ('content_html', models.TextField(editable=False, verbose_name='正文 HTML')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, '文章'), (1, '页面')], default=0, verbose_name='文章类型')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建日期')),
                ('updated_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='修改日期')),
                ('outline', models.TextField(blank=True, null=True, verbose_name='提纲')),
                ('tags', models.ManyToManyField(to='pyblog.Tag', verbose_name='标签')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
    ]