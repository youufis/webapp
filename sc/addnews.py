from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from sc.models import *
from DjangoUeditor.widgets import UEditorWidget
from DjangoUeditor.forms import UEditorField, UEditorModelForm

catelist = cate.objects.all()


class newsform(forms.Form):
    cate = forms.ModelChoiceField(
        queryset=catelist, label="类别", initial=catelist.first().name)
    title = forms.CharField(max_length=100, label="标题",
                            widget=widgets.TextInput(attrs={'size': '80'}))
    content = forms.CharField(label="内容", widget=UEditorWidget(
        {"width": 600, "height": 300,
         "imagePath": 'images/', "filePath": 'upfiles/', "toolbars": "mini"}))
    # toolbars:full(default), besttome, mini and normal!')
