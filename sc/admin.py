from django.contrib import admin
from .models import *
# Register your models here.
class cateadmin(admin.ModelAdmin):
    list_display=['id','name']
    list_per_page = 20
class newsadmin(admin.ModelAdmin):
    list_display=['id','title','cate','user','create_time','create_date','status']
    list_per_page = 20

    #返回当前用户发布内容的数据集
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

class ipinfoadmin(admin.ModelAdmin):
    list_display=['id','caption','ipaddr','create_time']
    list_per_page = 20


admin.site.register(cate,cateadmin)
admin.site.register(news,newsadmin)
admin.site.register(ipinfo,ipinfoadmin)