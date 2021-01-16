from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from sc.models import *
from DjangoUeditor.widgets import UEditorWidget
from DjangoUeditor.forms import UEditorField, UEditorModelForm

#普通用户发布和修改内容表单
class newsform(forms.Form):
    catelist = cate.objects.all()
    cate = forms.ModelChoiceField(
        queryset=catelist, label="类别", initial=catelist.first().name)

    title = forms.CharField(max_length=100, label="标题",
                            widget=widgets.TextInput(attrs={'size': '50%'}))
    img=forms.ImageField(label="图片封面",allow_empty_file=True,required=False)
    content = forms.CharField(label="内容", widget=UEditorWidget(
        {"width":"98%", "height": 400,
         "imagePath": 'pic/', "filePath": 'upfiles/'}))
    # toolbars:full(default), besttome, mini and normal!')

#用户上传文件
class fileform(forms.Form):
    file=forms.FileField(label="文件上传：")

#普通用户发布和修改产品表单
class productform(forms.Form):
    name = forms.CharField(max_length=100, label="产品名称",
                            widget=widgets.TextInput(attrs={'size': '50%'}))
    img=forms.ImageField(label="产品图片",allow_empty_file=True,required=False)
    price=forms.IntegerField(label="产品价格")
    repository=forms.ChoiceField(label="库存",choices=(("无货", "无货"), ("有货", "有货")),initial="有货" )
    content = forms.CharField(label="产品详情", widget=UEditorWidget(
        {"width":"98%", "height": 400,
         "imagePath": 'pic/', "filePath": 'upfiles/'}))

#留言
class msgbookform(forms.Form):
    msg=forms.CharField(max_length=150, label="留言", widget=widgets.Textarea(attrs={'cols':50,'rows':5}))
