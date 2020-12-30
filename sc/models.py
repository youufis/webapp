from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
# Create your models here.


class cate(models.Model):
    name = models.CharField(verbose_name="分类名称", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "分类名称"
        verbose_name_plural = verbose_name


class news(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    content = UEditorField(verbose_name='内容', width=600, height=400,imagePath='images/',filePath='upfiles/',default='')
    cate = models.ForeignKey(cate, verbose_name="分类", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="时间", auto_now_add=True)
    create_date = models.DateField(verbose_name="日期", auto_now_add=True)
    status = models.CharField(verbose_name="审核", choices=(
        ("未审核", "未审核"), ("已审核", "已审核")), max_length=10, default="未审核")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = verbose_name

class ipinfo(models.Model):
    caption=models.CharField(verbose_name="地址",max_length=20,default="IP")
    ipaddr=models.GenericIPAddressField(verbose_name="IP地址")
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)
    create_date=models.DateTimeField(verbose_name="日期",auto_now_add=True)

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name="地址"
        verbose_name_plural=verbose_name
    