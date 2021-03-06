from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from sc.models import *
from DjangoUeditor.widgets import UEditorWidget
from DjangoUeditor.forms import UEditorField, UEditorModelForm

#普通用户发布和修改内容表单
class newsform(forms.Form):
    catelist = cate.objects.filter(pcate__isnull=False)#二级和三级分类
    fcatelist=cate.objects.filter(pcate__isnull=True)#一级分类
    scatelist=cate.objects.filter(pcate__in=fcatelist)#二级分类
    tcatelist=cate.objects.filter(pcate__in=scatelist)#三级分类

    stcatelist=scatelist|tcatelist#二级和三级分类合并
   
    cate = forms.ModelChoiceField(
        queryset=stcatelist, label="类别", initial=catelist.first().name)

    title = forms.CharField(max_length=100, label="标题",
                            widget=widgets.TextInput(attrs={'size': '50%'}))
    img=forms.ImageField(label="图片封面",allow_empty_file=True,required=False)
    content = forms.CharField(label="内容", widget=UEditorWidget(
        {"width":"98%", "height": 400,
         "imagePath": 'pic/', "filePath": 'upfiles/'}))
    # toolbars:full(default), besttome, mini and normal!')

#用户上传文件
class fileform(forms.Form):
    catelist=filecate.objects.filter(cate__isnull=True)
    cate=forms.ModelChoiceField(queryset=catelist,label="文件分类",initial=catelist.first().name)   
    file=forms.FileField(label="文件上传：")

#用户上传图像
class imgform(forms.Form):
    image=forms.ImageField(label="图像上传：")

#普通用户发布和修改产品表单
class productform(forms.Form):
    catelist=productcate.objects.filter(cate__isnull=False)
    name = forms.CharField(max_length=100, label="产品名称",
                            widget=widgets.TextInput(attrs={'size': '50%'}))
    cate=forms.ModelChoiceField(queryset=catelist,label="类别",initial=catelist.first().name)
    img=forms.ImageField(label="产品图片",allow_empty_file=True,required=False)
    price=forms.IntegerField(label="产品价格",initial=100)
    repository=forms.ChoiceField(label="库存",choices=(("无货", "无货"), ("有货", "有货")),initial="有货" )
    content = forms.CharField(label="产品详情", widget=UEditorWidget(
        {"width":"98%", "height": 400,
         "imagePath": 'pic/', "filePath": 'upfiles/'}))

#留言
class msgbookform(forms.Form):
    msg=forms.CharField(max_length=150, label="留言", widget=widgets.Textarea(attrs={'cols':50,'rows':5}))
