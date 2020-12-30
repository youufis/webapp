from django.contrib import admin
from .models import *
# Register your models here.
class cateadmin(admin.ModelAdmin):
    list_display=['id','name']
class newsadmin(admin.ModelAdmin):
    list_display=['id','title','cate','create_time','create_date','status']
class ipinfoadmin(admin.ModelAdmin):
    list_display=['id','caption','ipaddr','create_time','create_date']

admin.site.register(cate,cateadmin)
admin.site.register(news,newsadmin)
admin.site.register(ipinfo,ipinfoadmin)