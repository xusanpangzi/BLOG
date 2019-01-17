from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.six import python_2_unicode_compatible
from django.contrib.auth.models import User
from Blog import settings
@python_2_unicode_compatible
class User(AbstractUser):

    nickname = models.CharField(max_length=50, blank=True)
    email = models.EmailField('邮箱', unique=True, error_messages={'unique': "该邮箱地址已被占用。", }, )

    class Meta(AbstractUser.Meta):
        pass
