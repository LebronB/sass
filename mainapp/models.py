from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    email = models.EmailField(max_length=32, verbose_name="邮箱")
    mobile_phone = models.CharField(max_length=32, verbose_name="手机号码")
    password = models.CharField(max_length=32, verbose_name="密码")