import re

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from joplin import models as models_joplin
from pyblog import models as models_blog


class Command(BaseCommand):
    last_sync_at = 0
    pattern_resource = re.compile(r'(\[.*\]\()(:/)([a-z0-9]+)?(\))')
    source_url_prefix = settings.JOPLIN_MEDIA_URL_PREFIX

    def add_arguments(self, parser):
        parser.add_argument('-i', '--interval', type=int, help='Sync interval', default=5)
        parser.add_argument('--force', action='store_true', help='Update all note')

    def handle(self, *args, **options):
        if not options['force']:
            self.last_sync_at = (timezone.now().timestamp() - options['interval'] * 60) * 1000
        self.sync_tags()
        note_query = models_joplin.Note.objects.filter(updated_time__gt=self.last_sync_at,
                                                       source_url__isnull=False).exclude(source_url='')
        for note in note_query:
            post, created = models_blog.Post.objects.update_or_create(uid=note.id,
                                                                      defaults=self.parse_note_to_post_dict(note))
            post_tags = models_blog.Tag.objects.filter(uid__in=list(note.tags.values_list('id', flat=True)))
            post.tags.set(post_tags)
        self.delete_redundant_post()

    def sync_tags(self):
        joplin_tags = models_joplin.Tag.objects.filter(updated_time__gt=self.last_sync_at)
        for tag_j in joplin_tags:
            models_blog.Tag.objects.update_or_create(uid=tag_j.id, defaults={'title': tag_j.title})

    def parse_note_to_post_dict(self, note):
        return {
            "is_published": True,
            "title": note.title,
            "slug": note.source_url,
            "content": self.pattern_resource.sub(self.pares_img_url, note.body),
            "created_time": self._ts_to_datetime(note.user_created_time),
            "updated_time": self._ts_to_datetime(note.user_updated_time)
        }

    def pares_img_url(self, body):
        resource = models_joplin.Resource.objects.get(id=body.group(3))
        return f'{body.group(1)}{self.source_url_prefix}{body.group(3)}.{resource.file_extension}{body.group(4)}'

    @staticmethod
    def delete_redundant_post():
        notes_ids = list(models_joplin.Note.objects.filter(
            source_url__isnull=False).exclude(source_url='').values_list('id', flat=True))
        models_blog.Post.objects.exclude(uid__in=notes_ids).delete()

    @staticmethod
    def _ts_to_datetime(ts):
        return timezone.datetime.fromtimestamp(ts / 1000)
