from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class MyUser(AbstractUser): # 继承AbstractUser类，实际上django的User也是继承他，我们要做的就是用自己的类代替django自己的User
    name = models.CharField(u'昵称', max_length=32, blank=False, null=True)
    publicinfo=models.CharField(u'个性签名', max_length=32,blank=True, null=True,default='博主很懒，没有说什么')
    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u"用户信息"
    def __str__(self):
        return self.username
