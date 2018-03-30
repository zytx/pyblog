from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group as GroupModel
from django.core.mail import send_mail


class UserManager(BaseUserManager):

    def create_user(self, email, nickname, password=None):
        """
        新建用户
        """
        if not email:
            raise ValueError('必须有一个Email，用作账户名')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        """
        新建超级用户
        """
        user = self.create_user(
            email,
            password=password,
            nickname=nickname
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    用户模型
    Email为用户名
    """
    email = models.EmailField('邮箱', max_length=50, unique=True)
    nickname = models.CharField('昵称', max_length=30)
    url = models.URLField('网站', null=True, blank=True)
    level = models.PositiveIntegerField('等级', default=0)
    reg_date = models.DateTimeField('注册日期', auto_now=True)

    is_active = models.BooleanField('可用状态', default=True)
    is_staff = models.BooleanField('职员状态', default=False, help_text='指明该用户能否登录后台管理')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def get_full_name(self):
        # The user is identified by their email address
        return self.nickname

    def get_short_name(self):
        # The user is identified by their email address
        return self.nickname

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Group(GroupModel):
    class Meta:
        proxy = True
        verbose_name = '组'
        verbose_name_plural = '组'
