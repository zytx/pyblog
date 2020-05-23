import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'pyblog',
    'comment',
    'editormd',
    'authentication',
    'joplin'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pyblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/templates", ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'pyblog.context_processors.info'
            ],
        },
    },
]

WSGI_APPLICATION = 'pyblog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# 'create database db_name default character set utf8mb4 collate utf8mb4_unicode_ci;'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT', '3306'),
        'OPTIONS': {'charset': 'utf8mb4'},
    },
    'joplin': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv('JOPLIN_DATABASE_NAME'),
    }
}

DATABASE_ROUTERS = ['joplin.router.db_router.JoplinRouter']

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # 其检查密码和用户的一组属性之间的相似性
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # 检查密码是否满足最小长度
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        # 检查密码是否出现在通用密码列表中，默认情况下，它与包含的1000个常用密码列表进行比较
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # 检查密码是否不是完全数字的
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Email
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', True)

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', "Mr.Z's Blog")
EMAIL_BACK_DOMAIN = os.getenv('EMAIL_BACK_DOMAIN', os.getenv('DOMAIN_NAME', 'www.immrz.com'))

AUTH_USER_MODEL = 'authentication.User'

# 是否给URL添加一个结尾的斜线. 只有安装了 CommonMiddleware 之后,该选项才起作用
APPEND_SLASH = True

SITE_TITLE = os.getenv('SITE_TITLE', "Mr.Z' Blog")
SITE_SUMMARY = os.getenv('SITE_SUMMARY', "I'm Mr.Z")

INDEX_KEYWORDS = os.getenv('INDEX_KEYWORDS', '个人博客')
INDEX_DESCRIPTION = os.getenv('INDEX_DESCRIPTION', 'Mr.Z的个人博客')

DOMAIN_NAME = os.getenv('DOMAIN_NAME', 'www.immrz.com')

if not DEBUG:
    STATICFILES_STORAGE = 'qcloudcos.storage.StaticStorage'  # 静态文件存储后端
    # DEFAULT_FILE_STORAGE = 'qcloudcos.storage.MediaStorage'  # 上传文件存储后端

STORAGE_OPTION = {
    'STATIC': {
        'appid': os.getenv('STATIC_APP_ID'),
        'secretID': os.getenv('STATIC_SECRET_ID'),
        'secretKey': os.getenv('STATIC_SECRET_KEY'),
        'region': os.getenv('STATIC_REGION'),
        'bucket': os.getenv('STATIC_BUCKET'),
        'cdn': os.getenv('STATIC_CDN', True),
        'ci': os.getenv('STATIC_CI', False),
        'dir': os.getenv('STATIC_DIR', '/'),
        'domain': os.getenv('STATIC_DOMAIN', '//static.immrz.com')
    },
    'MEDIA': {
        'appid': os.getenv('MEDIA_APP_ID'),
        'secretID': os.getenv('MEDIA_SECRET_ID'),
        'secretKey': os.getenv('MEDIA_SECRET_KEY'),
        'region': os.getenv('MEDIA_REGION'),
        'bucket': os.getenv('MEDIA_BUCKET'),
        'cdn': os.getenv('MEDIA_CDN', True),
        'ci': os.getenv('MEDIA_CI', True),
        'dir': os.getenv('MEDIA_DIR', '/'),
        'domain': os.getenv('MEDIA_DOMAIN', '//media.immrz.com')
    }
}

JOPLIN_MEDIA_URL_PREFIX = os.getenv('JOPLIN_MEDIA_URL_PREFIX')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S"
}

RECAPTCHA_SECRET = os.getenv('RECAPTCHA_SECRET')
RECAPTCHA_LEVEL = 0.7

try:
    from .settings_local import *
except Exception:
    pass
