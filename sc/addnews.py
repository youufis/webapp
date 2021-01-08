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
                            widget=widgets.TextInput(attrs={'size': '80'}))
    content = forms.CharField(label="内容", widget=UEditorWidget(
        {"width": 800, "height": 400,
         "imagePath": 'images/', "filePath": 'upfiles/', "toolbars": "mini"}))
    # toolbars:full(default), besttome, mini and normal!')
