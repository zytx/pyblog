import os
from django.conf import settings
from django.core.files.storage import Storage
from qcloudcos.cos.cos_client import CosS3Client, CosConfig
from datetime import datetime
from django.utils import timezone
import mimetypes


class QcloudStorage(Storage):
    """
    该类只能被继承，并定义option
    """
    option = {}
    root = settings.STATIC_URL or settings.MEDIA_URL

    def __init__(self):
        self.config = CosConfig(
            Appid=self.option['appid'],
            Region=self.option['region'],
            Access_id=self.option['secretID'],
            Access_key=self.option['secretKey']
        )
        self.client = CosS3Client(self.config)

    def _open(self, name):
        name = self._normalize_name(name)
        response = self.client.get_object(Bucket=self.option['bucket'], Key=name)
        return response['Body'].get_raw_stream()

    def _save(self, name, content):
        u = self._normalize_name(name)
        self.client.put_object(
            Bucket=self.option['bucket'],
            Body=content.read(),
            Key=u,
            ContentType=mimetypes.guess_type(u, strict=False)[0]
        )
        return name

    def _normalize_name(self, name):
        return self.option.get('dir', self.root) + name

    def generate_filename(self, filename):
        dir_name, filename = os.path.split(filename)
        return os.path.normpath(os.path.join(dir_name, self.get_valid_name(filename))).replace('\\', '/')  # Windows路径转换

    def exists(self, name):
        name = self._normalize_name(name)
        try:
            self.client.head_object(
                Bucket=self.option['bucket'],
                Key=name
            )
        except:
            return False
        return True

    def delete(self, name):
        name = self._normalize_name(name)
        self.client.delete_object(
            Bucket=self.option['bucket'],
            Key=name
        )

    def get_created_time(self, name):
        name = self._normalize_name(name)
        response = self.client.head_object(
            Bucket=self.option['bucket'],
            Key=name
        )
        dt = timezone.make_aware(datetime.strptime(response['date'], '%a, %d %b %Y %H:%M:%S %Z'),
                                 timezone.get_fixed_timezone(0))
        return dt if settings.USE_TZ else timezone.make_naive(dt)

    def get_modified_time(self, name):
        name = self._normalize_name(name)
        response = self.client.head_object(
            Bucket=self.option['bucket'],
            Key=name
        )
        dt = timezone.make_aware(datetime.strptime(response['last-modified'], '%a, %d %b %Y %H:%M:%S %Z'),
                                 timezone.get_fixed_timezone(0))
        return dt if settings.USE_TZ else timezone.make_naive(dt)

    def url(self, name):
        name = self._normalize_name(name)

        if self.option.get('domain', False):
            return self.option['domain'] + name

        region = self.option['region']

        if self.option.get('ci') and self.option.get('cdn'):
            region = 'image'  # 万象优图CDN
        elif self.option.get('ci'):
            region = 'picsh'  # 万象优图
        elif self.option.get('cdn'):
            region = 'file'  # 对象存储CDN
        else:
            if region == 'ap-beijing-1':
                region = 'tj'
            elif region == 'ap-beijing':
                region = 'bj'
            elif region == 'ap-shanghai':
                region = 'sh'
            elif region == 'ap-guangzhou':
                region = 'gz'
            elif region == 'ap-chengdu':
                region = 'cd'
            elif region == 'ap-singapore':
                region = 'sgp'
            elif region == 'ap-hongkong':
                region = 'hk'
            elif region == 'na-toronto':
                region = 'ca'
            elif region == 'eu-frankfurt':
                region = 'ger'
            region = 'cos' + region  # 对象存储

        url = "{protocol}//{bucket}-{uid}.{region}.myqcloud.com{path}".format(
            protocol=self.option.get('protocol', ''),
            bucket=self.option['bucket'],
            uid=self.option['appid'],
            region=region,
            path=name
        )
        return url

    def listdir(self, path='/'):
        response = self.client.list_objects(
            Bucket=self.option['bucket'],
            Prefix=path
        )
        files = []
        dirs = set()
        base_parts = path.split("/")[:-1]
        for item in response['Contents']:
            parts = item['Key'].split("/")
            parts = parts[len(base_parts):]
            if len(parts) == 1:
                # File
                files.append(parts[0])
            elif len(parts) > 1:
                # Directory
                dirs.add(parts[0])
        return list(dirs), files

    def size(self, name):
        response = self.client.head_object(
            Bucket=self.option['bucket'],
            Key=name
        )
        sizes = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        dblbyte = bytes_num = int(response['Content-Length'])
        while i < len(sizes) and bytes_num >= 1024:
            dblbyte = bytes_num / 1024.0
            i = i + 1
            bytes_num = bytes_num / 1024

        return str(round(dblbyte, 2)) + " " + sizes[i]


class StaticStorage(QcloudStorage):
    option = settings.STORAGE_OPTION['STATIC']
    root = settings.STATIC_URL


class MediaStorage(QcloudStorage):
    option = settings.STORAGE_OPTION['MEDIA']
    root = settings.MEDIA_URL if settings.MEDIA_URL else settings.STATIC_URL
