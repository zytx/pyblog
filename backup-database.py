from pyblog import settings
from datetime import datetime, timedelta, timezone
from qcloudcos.cos.cos_client import CosS3Client, CosConfig
import os


cos_config = settings.STORAGE_OPTION['BACKUP']
client = CosS3Client(CosConfig(
            Appid = cos_config['appid'],
            Region = cos_config['region'],
            Access_id = cos_config['secretID'],
            Access_key = cos_config['secretKey']
        ))

db_config = settings.DATABASES['default']
file_path = '/tmp/pyblog.sql.gz'
os.system("mysqldump -u%s %s --databases %s -h%s -P%s 2>/dev/null | gzip > %s" % (
        db_config['USER'],
        '-p%s' % db_config['PASSWORD'] if db_config['PASSWORD'] else '',
        db_config['NAME'],
        db_config['HOST'],
        db_config['PORT'],
        file_path
    ))

with open(file_path, 'rb') as fp:
    response = client.put_object(
        Bucket = cos_config['bucket'],
        Body = fp,
        Key = '/pyblog/sql/' + datetime.now(timezone(timedelta(hours=8))).strftime("%Y/%m/%d/%Y-%m-%d_%H_%M_%S") + '.sql.gz'
    )
