from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from sc.models import *

class imgform(forms.Form):
    image=forms.ImageField(label="图像上传：")

class fileform(forms.Form):
    file=forms.FileField(label="文件上传：")