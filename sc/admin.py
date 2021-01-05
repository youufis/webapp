from django.contrib import admin
from .models import *
# Register your models here.
class cateadmin(admin.ModelAdmin):
    list_display=['id','name']
    list_per_page = 20
class newsadmin(admin.ModelAdmin):
    exclude = ('user',)#排除
    list_display=['id','title','cate','user','create_time','create_date','status']
    list_per_page = 20

    #自定义actions 审核发布
    actions=['query_status']
    def query_status(self,request,queryset):       
        queryset.update(status="已审核")       

    query_status.short_description="审核所选的 内容"

    #返回当前用户发布内容的数据集
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def instance_forms(self):
        super().instance_forms()
    # 判断是否为新建操作，新建操作才会设置status的默认值
        if not self.org_obj:
            self.form_obj.initial['status']="已审核"

    #自动保存登录用户
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
            obj.save()
 
    search_fields = ['title','user__username','status'] # 按文章title和用户user搜索

class ipinfoadmin(admin.ModelAdmin):
    list_display=['id','caption','ipaddr','create_time']
    list_per_page = 20


admin.site.register(cate,cateadmin)
admin.site.register(news,newsadmin)
admin.site.register(ipinfo,ipinfoadmin)

