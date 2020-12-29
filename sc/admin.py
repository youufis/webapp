from django.contrib import admin
from .models import *
# Register your models here.
class cateadmin(admin.ModelAdmin):
    list_display=['id','name']
class newsadmin(admin.ModelAdmin):
    list_display=['id','title','cate','create_time','create_date','status']

admin.site.register(cate,cateadmin)
admin.site.register(news,newsadmin)