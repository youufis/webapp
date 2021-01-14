from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from django.conf import settings
import os
# Create your models here.



class cate(models.Model):
    name = models.CharField(verbose_name="分类", max_length=20)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "内容分类"
        verbose_name_plural = verbose_name

#存放已审核过的图片文件名
class auditimg(models.Model):
    imgname=models.CharField(verbose_name="文件名",max_length=50)   

    def __str__(self):
        return self.imgname
    class Meta:
        verbose_name="审核图像"
        verbose_name_plural=verbose_name

class news(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    img=models.ImageField(verbose_name="图片封面",upload_to="images/",blank=True,null=True)
    content = UEditorField(verbose_name='内容', width='100%', height=400,imagePath='pic/',filePath='upfiles/',default='')
    cate = models.ForeignKey(cate, verbose_name="分类", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='用户',related_name='user',on_delete=models.CASCADE,blank=True,null=True)
    create_time = models.DateTimeField(verbose_name="时间", auto_now_add=True)
    create_date = models.DateField(verbose_name="日期", auto_now_add=True)
    status = models.CharField(verbose_name="审核", choices=(
        ("未审核", "未审核"), ("已审核", "已审核")), max_length=10, default="未审核")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "新闻内容"
        verbose_name_plural = verbose_name

class ipinfo(models.Model):
    caption=models.CharField(verbose_name="地址",max_length=20,default="IP")
    ipaddr=models.GenericIPAddressField(verbose_name="IP地址")
    num=models.IntegerField(verbose_name="次数",blank=True,null=True)
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)
    
    

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name="访问地址"
        verbose_name_plural=verbose_name

class newshits(models.Model):
    news=models.ForeignKey(news,verbose_name="热度",on_delete=models.CASCADE)
    num=models.IntegerField(verbose_name="次数",blank=True,null=True)
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)
   

#让上传的文件路径动态地与user的名字有关
def upload_to(instance,filename):
    return os.path.join(instance.username,filename)
#用户单独上传文件管理
class userfile(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=50)
    name = models.CharField(max_length=150,null=True)
    file=models.FileField(verbose_name="文件",upload_to=upload_to)
    size=models.IntegerField(verbose_name="大小",blank=True,null=True)
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)
    
    def __str__(self):
        return self.username
    class Meta:
        verbose_name="用户文件"
        verbose_name_plural=verbose_name
#产品
class product(models.Model):
    name=models.CharField(verbose_name="产品名称",max_length=150)
    img=models.ImageField(verbose_name="产品图片",upload_to="pic/")
    content = UEditorField(verbose_name='产品详情', width='100%', height=400,imagePath='pic/',filePath='upfiles/',default='')
    user = models.ForeignKey(User,verbose_name='用户',on_delete=models.CASCADE)
    price=models.IntegerField(verbose_name="价格")
    repository= models.CharField(verbose_name="库存", choices=(("无货", "无货"), ("有货", "有货")), max_length=10, default="有货")
    status= models.CharField(verbose_name="审核", choices=(
        ("未审核", "未审核"), ("已审核", "已审核")), max_length=10, default="未审核")
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name="产品名称"
        verbose_name_plural=verbose_name

    

    