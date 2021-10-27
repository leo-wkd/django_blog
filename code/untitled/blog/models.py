from django.db import models
from user.models import MyUser
from mdeditor.fields import MDTextField
import django.utils.timezone as timezone
# Create your models here.
class Blog(models.Model):
    bloguser=models.ForeignKey(MyUser,related_name='bloguser',on_delete=models.CASCADE,verbose_name="博主")
    time=models.DateTimeField(verbose_name='发表时间', default = timezone.now)
    title=models.CharField(u'博客标题', max_length=32, blank=False,)
    bloginfo=models.TextField(u'博客说明', blank=True, null=True)
    blogtext = MDTextField(u'内容',config_name='default')
    viewnum=models.IntegerField(verbose_name='浏览量')
    class Meta:
        verbose_name = u'博客信息'
        verbose_name_plural = u"博客信息"
    def __str__(self):
        return self.title
