from django.contrib import admin
from .models import *
from .views import *

# Register your models here.

#修改网页title和站点header。
admin.site.site_title = "管理后台"
admin.site.site_header = "控制台"

#类别与内容数据表在同一页上
#class newsInline(admin.TabularInline):
    #model=news
    #fields=('title', 'status', )
#网站配置
class bconfigadmin(admin.ModelAdmin):
    list_display=['id','name','isimgaudit','isspider','ismsg','ismsgaudit','isimgai','islogin','isregister','totalsize']

#用户扩展资料
class  userextendadmin(admin.ModelAdmin):
    list_display=['id','user','storage','ispublishnews','ispublishprod','isupfile']
    list_per_page=20

#分类
class cateadmin(admin.ModelAdmin):
    list_display=['id','name',"pcate"]
    list_per_page = 20
    #inlines = [newsInline, ]


#内容
class newsadmin(admin.ModelAdmin):
    exclude = ('user','keyword',)#排除
    list_display=['id','title','img','cate','user','create_time','status',"keyword"] #可显示的字段
    
    list_filter=('status','create_time') #过滤选项
    ordering=('-id','title','create_time','cate','user') # 排序字段
    list_per_page = 20
  
    #自定义actions 审核发布
    actions=['query_status']
    def query_status(self,request,queryset):       
        queryset.update(status="已审核")       

    
    #显示名称
    query_status.short_description="审核所选的 内容"
    

    #返回当前用户发布内容的数据集
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
   
    #对外键进行设置初值
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):                                                                                                             
        if db_field.name == 'cate':   
            catelist = cate.objects.filter(pcate__isnull=False)
            fcatelist=cate.objects.filter(pcate__isnull=True)
            scatelist=cate.objects.filter(pcate__in=fcatelist)
            tcatelist=cate.objects.filter(pcate__in=scatelist)
            stcatelist=scatelist|tcatelist
            kwargs['queryset']= stcatelist                                              
            kwargs['initial'] = cate.objects.filter(pcate__isnull=False).first()   
                              
        return super(newsadmin, self).formfield_for_foreignkey(                     
            db_field, request, **kwargs )
    
    #对字段进行设置初值
    def formfield_for_dbfield(self, db_field, **kwargs):
        field =  super(newsadmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'status':
            field.initial = '已审核'
        return field    
    
   
    #自动保存登录用户
    def save_model(self, request, obj, form, change):        
        obj.user = request.user
        obj.save()
   

    # 按文章title和用户user搜索
    search_fields = ['title','user__username','status'] 
  

#登录ip信息
class ipinfoadmin(admin.ModelAdmin):
    list_display=['id','caption','ipaddr','num','create_time']
    list_per_page = 20

#已审核图像信息
class auditimgadmin(admin.ModelAdmin):
    list_display=['id','imgname']
    list_per_page = 20


#用户上传文件信息
class userfileadmin(admin.ModelAdmin):
    list_display=['id','username',"name","file","create_time"]
    list_per_page = 20

#产品类别
class productcateadmin(admin.ModelAdmin):
    list_display=['id','name','cate']
    list_per_page = 20



#产品
class productadmin(admin.ModelAdmin):
    exclude = ('user',)#排除
    list_display=['id','name','cate','user','img','price','repository','status','create_time']
    list_per_page=20

    list_filter=('status','create_time') #过滤选项
    ordering=('-id','name','create_time','cate','user') # 排序字段

     #自定义actions 审核发布
    actions=['query_status']
    def query_status(self,request,queryset):       
        queryset.update(status="已审核")     

    #显示名称
    query_status.short_description="审核所选的 内容"

        #自动保存登录用户
    def save_model(self, request, obj, form, change):        
        obj.user = request.user
        obj.save()

    
    #显示名称
    query_status.short_description="审核所选的 内容"

        #返回当前用户发布内容的数据集
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
   
    #对外键进行设置初值
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):                                                                                                             
        if db_field.name == 'cate':                                                
            kwargs['initial'] =productcate.objects.filter(cate__isnull=False).first()
            kwargs['queryset']= productcate.objects.filter(cate__isnull=False)                               
        return super(productadmin, self).formfield_for_foreignkey(                     
            db_field, request, **kwargs )
    
    #对字段进行设置初值
    def formfield_for_dbfield(self, db_field, **kwargs):
        field =  super(productadmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'status':
            field.initial = '已审核'
        return field

     # 按产品和用户user搜索
    search_fields = ['name','user__username','status'] 

#用户留言
class msgbookadmin(admin.ModelAdmin):
    list_display=['id','user','msg','ipaddr','status','create_time']
    list_per_page=20

     #自定义actions 审核发布
    actions=['query_status']
    def query_status(self,request,queryset):       
        queryset.update(status="已审核")     

    #显示名称
    query_status.short_description="审核所选的 内容"

admin.site.register(cate,cateadmin)
admin.site.register(news,newsadmin)
admin.site.register(ipinfo,ipinfoadmin)
admin.site.register(auditimg,auditimgadmin)
admin.site.register(userfile,userfileadmin)
admin.site.register(product,productadmin)
admin.site.register(productcate,productcateadmin)
admin.site.register(msgbook,msgbookadmin)
admin.site.register(bconfig,bconfigadmin)
admin.site.register(userextend,userextendadmin)

