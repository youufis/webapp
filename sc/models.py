from django.db import models
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField
from django.conf import settings
import os
# Create your models here.

#内容分类
class cate(models.Model):
    name = models.CharField(verbose_name="分类", max_length=20)
    pcate=models.ForeignKey('self',null=True,blank=True,verbose_name="父分类", on_delete=models.CASCADE)
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
#内容
class news(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    img=models.ImageField(verbose_name="图片封面",upload_to="images/",blank=True,null=True)
    content = UEditorField(verbose_name='内容', width='100%', height=400,imagePath='pic/',filePath='upfiles/',default='')
    cate = models.ForeignKey(cate, verbose_name="分类", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='用户',related_name='user',on_delete=models.CASCADE,blank=True,null=True)
    create_time = models.DateTimeField(verbose_name="时间", auto_now_add=True)   
    status = models.CharField(verbose_name="审核", choices=(
        ("未审核", "未审核"), ("已审核", "已审核")), max_length=10, default="未审核")
    keyword=models.CharField(verbose_name="关键词", max_length=100, null=True,blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "内容详情"
        verbose_name_plural = verbose_name



#来访信息
class ipinfo(models.Model):
    caption=models.CharField(verbose_name="地址",max_length=20,default="IP")
    ipaddr=models.GenericIPAddressField(verbose_name="IP地址")
    num=models.IntegerField(verbose_name="次数",blank=True,null=True)
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)
    
    

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name="访问记录"
        verbose_name_plural=verbose_name

###访问量
class newshits(models.Model):
    news=models.ForeignKey(news,verbose_name="热度",on_delete=models.CASCADE)
    num=models.IntegerField(verbose_name="次数",blank=True,null=True)
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)

   
#文件分类
class filecate(models.Model):
    name= models.CharField(default="",max_length=30,verbose_name="类别名")   
    cate=models.ForeignKey('self',null=True,blank=True,verbose_name="父分类", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "文件类别"
        verbose_name_plural = verbose_name

#让上传的文件路径动态地与user的名字有关
def upload_to(instance,filename):
    return os.path.join(instance.username,filename)
#用户单独上传文件管理
class userfile(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=50)
    name = models.CharField(max_length=150,verbose_name="文件名",null=True)
    cate=models.ForeignKey(filecate,verbose_name="分类",null=True,blank=True,on_delete=models.CASCADE)
    file=models.FileField(verbose_name="文件",upload_to=upload_to)
    size=models.IntegerField(verbose_name="大小",blank=True,null=True)
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)
    
    def __str__(self):
        return self.username
    class Meta:
        verbose_name="用户文件"
        verbose_name_plural=verbose_name



#产品类别
class productcate(models.Model):   
    name= models.CharField(default="",max_length=30,verbose_name="类别名")   
    cate=models.ForeignKey('self',null=True,blank=True,verbose_name="父分类", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "产品类别"
        verbose_name_plural = verbose_name

#产品
class product(models.Model):
    name=models.CharField(verbose_name="产品名称",max_length=150)
    cate=models.ForeignKey(productcate,verbose_name="分类",null=True,blank=True,on_delete=models.CASCADE)
    img=models.ImageField(verbose_name="产品图片",upload_to="pic/",blank=True,null=True)
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
        verbose_name="产品详情"
        verbose_name_plural=verbose_name
#产品访问
class producthits(models.Model):
    product=models.ForeignKey(product,verbose_name="热度",on_delete=models.CASCADE)
    num=models.IntegerField(verbose_name="次数",blank=True,null=True)
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)    

#留言信息
class msgbook(models.Model):
    user=models.ForeignKey(User,verbose_name="用户",on_delete=models.CASCADE,blank=True,null=True)
    product=models.ForeignKey(product,verbose_name="产品",on_delete=models.CASCADE)
    msg=models.CharField(verbose_name="留言",max_length=150)
    ipaddr=models.GenericIPAddressField(verbose_name="IP地址")
    status= models.CharField(verbose_name="审核", choices=(
        ("未审核", "未审核"), ("已审核", "已审核")), max_length=10, default="未审核")
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add=True)

    def __str__(self):
        return self.ipaddr
    class Meta:
        verbose_name="用户留言"
        verbose_name_plural=verbose_name

#网站配置开关
class bconfig(models.Model):
    name=models.CharField(max_length=20,verbose_name="网站配置",default="config")
    isimgaudit=models.BooleanField(verbose_name="是否审核图像",default=False)
    isspider=models.BooleanField(verbose_name="是否抓取外部新闻",default=True)
    ismsg=models.BooleanField(verbose_name="是否开启留言",default=True)
    ismsgaudit=models.BooleanField(verbose_name="是否机器审核留言",default=True)
    isimgai=models.BooleanField(verbose_name="是否开启图像识别",default=True)
    islogin=models.BooleanField(verbose_name="是否开启登录",default=True)
    isregister=models.BooleanField(verbose_name="是否开启注册",default=True)
    totalsize=models.IntegerField(verbose_name="用户空间",default="104857600")#默认空间大小：100MB=100*1024*1024

    def __str__(self):
        return self.name
    class Meta:
        verbose_name="网站配置"
        verbose_name_plural=verbose_name

#扩展用户字段
class userextend(models.Model):
    user=models.ForeignKey(User,verbose_name="用户",on_delete=models.CASCADE)
    storage=models.IntegerField(verbose_name="存储空间",default="0")#默认空间大小：100MB=100*1024*1024bconfig.objects.get(name="config").totalsize
    ispublishnews=models.BooleanField(verbose_name="发布内容",default=True)
    ispublishprod=models.BooleanField(verbose_name="发布产品",default=True)
    isupfile=models.BooleanField(verbose_name="上传文件",default=True)
    create_time=models.DateTimeField(verbose_name="时间",auto_now_add="True")

 
    class Meta:
        verbose_name="用户扩展"
        verbose_name_plural=verbose_name