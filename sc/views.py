from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.exceptions import ValidationError
import os
from .models import *
from django.conf import settings
from sc.webforms import * #自定义表单
from django.contrib import messages
import random
import socket
from django.db.models import Q,F
import pandas as pd
import threading
import shutil
from django.db.models import Avg,Max,Min,Count,Sum  #   引入函数
#抓取外部数据
from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
from itertools import zip_longest

#########################获取IP############################################
def get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    return ip
##########################生成验证码###############################################
def check_code(request):
    import io
    from . import check_code as CheckCode
    stream = io.BytesIO()
    # img 图片对象, code 在图像中写的内容
    img, code = CheckCode.create_validate_code()
    img.save(stream, "png")
    # 图片页面中显示, 立即把 session 中的 CheckCode 更改为目前的随机字符串值
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())
###################用户注册登录登出##########################################
def logOut(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    return redirect(request.META['HTTP_REFERER'])

def logIn(request):
    #catelist=cate.objects.all()
    # 判断是否已经登录
    if request.user.is_authenticated:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        if request.method == 'GET':
            request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
            return render(request, 'login.html', locals())
        elif request.method == 'POST':
            username = request.POST.get("username", '')
            password = request.POST.get("password", '')
            if username != '' and password != '':
                user = authenticate(username=username, password=password)                               
                if user is not None:
                    login(request, user)
                    #print("登录成功！",user)                    
                    request.session["username"]=username
                    #print(request.session["username"])
                    #response.set_cookie('username',username) #使用response（用户自己电脑）保存的cookie来验证用户登录
                    return redirect(request.session['login_from'])
                else:
                    #print(username, password, user)
                    errormsg = '用户名或密码错误！'
                    return render(request, 'login.html', locals())
            else:
                return JsonResponse({"e": "chucuo"})

@csrf_exempt
def register(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
        return render(request, 'register.html', locals())
        #暂停用户注册
        #msg="暂停用户注册"
        #return render(request, 'base.html', locals())
    elif request.method == 'POST':
        # 接收表单数据
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')
        email = request.POST.get("email", '')
        checkcode = request.POST.get("check_code")
        # 判断数据是否正确
        if username != '' and password != '' and checkcode == request.session['CheckCode'].lower():
            # 判断用户是否存在
            if User.objects.filter(username=username).exists() == False:
                # 注册
                user = User.objects.create_user(
                    username=username, email=email, password=password) # is_staff=True激活用户登录后台

                user.save()
                #user.groups.add(name='publisher') #增加用户到publisher组（管理员后台中定义分配）（有管理自己发布内容的权限）
                my_group = Group.objects.get(name='publisher')
                my_group.user_set.add(user)
                #创建用户个人目录
                if not os.path.exists(os.path.join(settings.MEDIA_ROOT,username)):
                    os.makedirs(os.path.join(settings.MEDIA_ROOT,username))
                
                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                # 重定向跳转
    return redirect(request.session['login_from'], '/')

######################图像审核##############百度AI图像识别########################################   
def imgtoaudit():
    file_dir=os.path.join(settings.MEDIA_ROOT,"images")
    fname=random.sample(os.listdir(file_dir),4)        
    for img in fname:    
        fimg=auditimg.objects.filter(imgname=img)  #审核过的图像不用再审
        if not fimg.exists():   
            #print(img)   
            if imgaudit(img) in ['合规']: #图像审核通过存入图像库
                #fname[fname.index(img)]="audit.jpg"
                ret=auditimg.objects.get_or_create(
                    imgname=img,
                    )
            else: #不合规移动回收站
                fsrc=os.path.join(settings.MEDIA_ROOT,"images",img)
                fdst=os.path.join(settings.MEDIA_ROOT,"recycle",img)
                shutil.move(fsrc,fdst)
#调用百度内容审核
#conclusion	String	N	审核结果，可取值描述：合规、不合规、疑似、审核失败
#conclusionType	uint64	N	审核结果类型，可取值1、2、3、4，分别代表1：合规，2：不合规，3：疑似，4：审核失败
def imgaudit(img):    
    from aip import AipContentCensor
    #可以自行百度ai申请
    APP_ID = '23489175'
    API_KEY = 'ur1buDW12v3KvxUCZoFnWQNm'
    SECRET_KEY = 'iNIGdhkmlZka7ZgVwoZKOGmkS26umYpA'
    client = AipContentCensor(APP_ID, API_KEY, SECRET_KEY)
    #result = client.textCensorUserDefined("测试文本") #文本审核
    imgpath=os.path.join(settings.MEDIA_ROOT,"images",img)    
    with open(imgpath,"rb") as fp:
        img=fp.read()
    resultimg = client.imageCensorUserDefined(img)  
    #print(resultimg)
    return resultimg['conclusion']

def txtaudit(cont):    
    from aip import AipContentCensor
    #可以自行百度ai申请
    APP_ID = '23489175'
    API_KEY = 'ur1buDW12v3KvxUCZoFnWQNm'
    SECRET_KEY = 'iNIGdhkmlZka7ZgVwoZKOGmkS26umYpA'
    client = AipContentCensor(APP_ID, API_KEY, SECRET_KEY)
    result = client.textCensorUserDefined(cont)
    print(result)
    return result['conclusion']

#调用百度AI图像识别
def imgdetect(request,img):
    from aip import AipImageClassify
    """ 这里输入你创建应用获得的三个参数"""
    APP_ID = '15279946'
    API_KEY = 'gFT6Iim8OPT51HQFIyGOmIra'
    SECRET_KEY = 'Afi8SoHMFWSKYzi1QD78giGMyakVtr3k'
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

    imgpath=os.path.join(settings.MEDIA_ROOT,"images",img)
    imgurl="/media/images/"+img
    with open(imgpath,"rb") as fp:
        img=fp.read()
    options={}
    options["baike_num"] = 5
    resultimg=client.advancedGeneral(img,options)
    img_num=resultimg["result_num"]
    sclist=[]
    snamelist=[]
    baikeurllist=[]
    baikedeslist=[]
    for num in range(img_num):
        sc=str(round(resultimg["result"][num]["score"]*100,2))+"%"
        sname=resultimg["result"][num]["keyword"]
        if resultimg["result"][num]["baike_info"]:
            baikeurl=resultimg["result"][num]["baike_info"]["baike_url"]
            baikedes=resultimg["result"][num]["baike_info"]["description"]
        else:
            baikeurl="#"
            baikedes=""
        snamelist.append(sname)
        sclist.append(sc)
        baikeurllist.append(baikeurl)
        baikedeslist.append(baikedes)
    
    imginfo=zip(snamelist,sclist,baikeurllist,baikedeslist)

    return render(request,"imginfo.html",locals())

#定义一个图象审核线程，默认不开启
def timgtoaudit(bflag=False):
    if bflag:
        t = threading.Thread(target=imgtoaudit)       
        t.setDaemon(True)
        t.start()
    else:
        pass
######首页#######分类全局变量####支持三级下拉菜单############################################
#内容分类和产品分类全局变量
def global_params(request):
    #catelist=cate.objects.all()     
    catelist=cate.objects.filter(pcate__isnull=True)   # 一级分类
    flist=[]#一级分类
    for f in catelist:
        flist.append(f)

    slist=[]#二级分类
    tlist=[]#三分分类
    for s in flist:
        sp=cate.objects.filter(pcate__isnull=False,pcate=s.id)
        slist.append(sp) #二级分类     

    for t in slist: 
        tl=[]   
        for r in t:             
            tp=cate.objects.filter(pcate=r.id)#三级分类
            tl.append(tp)
        tlist.append(tl)
    
    newscatelist=list(zip_longest(flist,slist,tlist))
    ##############是否有三级分类##############################
    st=[]
    st1=[]
    st2=[]
    for s in slist:              
        for i in s:
            st1.append(i)
    
    for s in tlist:
        for i in s:
            for j in i:
                st2.append(j.pcate)
            
    ####先把二级分类和三级分类项保存在各自的列表中，然后求差集，得到有二级分类但无三级分类项
    st=list(set(st1)^set(st2))
    
    #print(st)
    ###########################################
    
    
    ####################产品分类##########################
    plist=productcate.objects.filter(cate__isnull=True)
    flist2=[]
    for f in plist:
        flist2.append(f)

    slist2=[]#二级分类
    tlist2=[]#三级分类    
    for s in flist2:
        sp=productcate.objects.filter(cate__isnull=False,cate=s.id)
        slist2.append(sp)

    for t in slist2:
        tl=[]
        for r in t:
            tp=productcate.objects.filter(cate=r.id)
            tl.append(tp)
        tlist2.append(tl)
#################是否有三级分类#################################################
    pst=[]
    pst1=[]
    pst2=[]
    for s in slist2:              
        for i in s:
            pst1.append(i)
    
    for s in tlist2:
        for i in s:
            for j in i:
                pst2.append(j.cate)
            
    
    pst=list(set(pst1)^set(pst2))
    #print(slist)    
    pslist=list(zip_longest(flist2,slist2,tlist2))

    
    return {
        "newscatelist":newscatelist,
        "st":st,
        "pslist":pslist,
        "pst":pst,
        }

#首页
def index(request):
    bflag=False #关闭开启线程审核封面图像
    timgtoaudit(bflag) #开启/关闭线程进行封面图像审核

  
    hostip=get_host_ip()
    clientip=get_client_ip(request)
    #来访ip记数
    if ipinfo.objects.filter(ipaddr__in=[clientip]):
       res = ipinfo.objects.update(num=F("num")+1)
    else:
        res=ipinfo.objects.create(
            ipaddr=clientip,
            num=1
        )
    #汇总所有ip访问次数
    #ret1= ipinfo.objects.annotate(total = Sum("num")).values("ipaddr","total")
    #ret2=ipinfo.objects.filter(ipaddr=clientip).first()
    #print(ret1,ret2)
    ret= ipinfo.objects.aggregate(total=Sum('num'))    
    hits=ret['total']

    #如果开启线程审核图像
    fname=[]
    if bflag:
        #图片随机展示
        fnameobj=auditimg.objects.all().order_by('?')[:3]    #图像库随机取4个
        for f in fnameobj:
            imgpath=os.path.join(settings.MEDIA_ROOT,"images",f.imgname)
            if not os.path.exists(imgpath):#如果不存在，删除图像库记录         
                ret=auditimg.objects.filter(imgname=f.imgname).delete()
            else:
                fname.append(f.imgname)
    else:
        fpath=os.path.join(settings.MEDIA_ROOT,'images')
        fname=random.sample(os.listdir(fpath),3) #封面目录随机取3图像
        #for f in os.listdir(fpath):
            #print(f)

    #最新封面
    fnamenewsobj=news.objects.filter(Q(img__isnull=False)&Q(status='已审核')).order_by("-id")[:3]

    #取出所有类别
    catelist=cate.objects.filter(pcate__isnull=False)
    newslist=[]
    #按类别返回内容
    for cateobj in catelist:        
        newslist.append(getPage(request,news.objects.filter(Q(cate=cateobj)&Q(status='已审核')).order_by("-create_time"),6))
    catenewslist=zip(catelist,newslist)

    #最新内容top6
    newstop6=news.objects.filter(status="已审核").order_by("-create_time")[:11]
    #最新热点top6
    newshit=newshits.objects.values("news").annotate(total=Count("id"))
    newshit= sorted(newshit, key=lambda k: k['total'],reverse = False)[:11]
    idhotlist=[]
    for idhot in newshit:
        idhotlist.append(idhot["news"])
    #print(idhotlist)
    newshot6=news.objects.filter(id__in=idhotlist).order_by('-id')

    ret=friendlylink() #默认url = "https://news.sina.com.cn/china/"
    #print(ret)

    producttop6=product.objects.filter(status="已审核").order_by("-create_time")[:6]

    return render(request,'index.html', locals())

#分页
def getPage(request, news_list,pagenum):
    paginator = Paginator(news_list, pagenum)
    try:
        page = int(request.GET.get('page', 1))
        news_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        news_list = paginator.page(1)
    return news_list
########类别页########详细页#################################################
#内容类别页
def newscate(request,cateid):
    cateobj=cate.objects.get(id=cateid)
    newslist=getPage(request,news.objects.filter(cate=cateobj).order_by('-create_time'),6)
    return render(request, "cate.html", locals())

 #内容详细页
def newsdetail(request,newsid):    
    newsobj=news.objects.get(id=newsid)    
    if newshits.objects.filter(news=newsobj):
       res = newshits.objects.update(num=F("num")+1)
    else:
        res=newshits.objects.create(
            news=newsobj,
            num=1
        )   
    #news_hits=newshits.objects.filter(news=newsobj).count
    news_hitsobj=newshits.objects.filter(news=newsobj).first()
    news_hits=news_hitsobj.num
    return render(request, "newsdetail.html", locals())

#############搜索###############################################################        
#标题搜索
def search(request):
    ctx ={}
    if request.POST:
        ctx['keywords'] = request.POST['q']
    res=ctx['keywords']
    newslist=getPage(request,news.objects.filter(title__contains= ctx['keywords']).order_by("-create_time"),10)
    return render(request,"result.html",locals())

#############excel批量导入用户####################################################
#excel批量导入用户
@csrf_exempt
@login_required
def uploadxls(request):
    if request.method=="POST":
        f=request.FILES['file']
        filepath = os.path.join(settings.MEDIA_ROOT,"upfiles",f.name)
        ext=f.name.split(".")[-1].lower()
        if ext not in ["xls","xlsx","csv"]:
            return render(request,'uploadxls.html',{"error":"上传文件类型错误"})
        else:
            with open(filepath,"wb") as fp:
                for info in f.chunks():
                    fp.write(info)
            
            data=pd.read_excel(filepath,sheet_name="Sheet1")
            row_count=data.shape[0]
            if row_count <1:
                return render(request,'uploadxls.html',{"error":"无可导入数据"})
            else:
                for row in range(row_count):
                    row_data=data.loc[row]
                    #print(row_data[0],row_data[1],row_data[2])
                    if User.objects.filter(username=row_data[0]).exists() == False:
                        user = User.objects.create_user(
                            username=row_data[0], email=row_data[1], password=str(row_data[2]))
                        user.save()
                    
                msg="数据导入成功"
                return render(request,'uploadxls.html',locals())    
    else:
        #加载表单
        return render(request,"uploadxls.html",locals())

#####用户内容页######删除内容#########编辑内容########发布和修改内容###################################
#普通用户内容页
@login_required
def usernews(request):    
    if request.session.get('username'):
        username= request.session["username"]
        userobj=User.objects.get(username=username)
        newslist=getPage(request,news.objects.filter(user=userobj).order_by('-create_time'),8)
        return render(request, "usernews.html",locals())
    else:
        return redirect("/logout/")

#删除内容
def delnews(request,newsid):
    ret=news.objects.filter(id=newsid).delete()
    return redirect('/usernews/')

#编辑内容
@csrf_exempt
@login_required
def editnews(request,newsid):
    newsobj=news.objects.get(id=newsid)
    context={
        'newsid':newsid,#内容id,传值到内容修改
        'newsitem':newsobj,
        'content_form':newsform().as_p #调用发布和修改内容表单
    }
    if request.method=="GET":
        return render(request, 'editnews.html', context=context)
    elif request.method=="POST":
        #news.objects.filter(id=newsid).update(**request.POST)
        return  redirect('/usernews/') #编辑成功后重定向到用户内容页

#普通用户发布和修改内容
@csrf_exempt
@login_required
def savenews(request):    
    #catelist=cate.objects.all()
    if request.method == 'POST':
        form = newsform(request.POST,request.FILES)
        if form.is_valid():
            data=form.cleaned_data
            data["user"]=User.objects.get(username=request.user.username)
            newsid=request.POST.get("newsid") #接收修改内容的id，如果id存在，就修改，否则就新增内容
            if news.objects.filter(id=newsid).exists():
                if not request.FILES:
                    data['img']=news.objects.filter(id=newsid).first().img
                else:
                    data['img']=request.FILES['img']
                #news.objects.filter(id=newsid).update(**data) #update会丢失img上传路径

                newsobj=news.objects.get(id=newsid)
                newsobj.user=data["user"]
                newsobj.cate=data["cate"]
                newsobj.title=data["title"]
                newsobj.img=data["img"]
                newsobj.content=data["content"]
                newsobj.save()

                messages.success(request, '修改成功')
                #return redirect("/usernews/") #根据需要可重定向页面
                return render(request,'webforms.html', {'form': form})
            else:
                news.objects.get_or_create(**data)
                messages.success(request, '发布成功,等待审核')
                return render(request,'webforms.html', {'form': form}) #
        else:
            #print(form.errors)
            clean_errors=form.errors.get("__all__")
            #print(222,clean_errors)
            return render(request,"webforms.html",{"form":form,"clean_errors":clean_errors})
    else:
        #加载表单
        title="内容发布与修改"
        form = newsform() 
        return render(request,'webforms.html', {'form': form,'title':title})

########抓取外部新闻链接############################################################################
# 抓取外部新闻链接    
def friendlylink(url="https://news.sina.com.cn/china/"):
    #url = "https://news.sina.com.cn/china/"
    f = requests.get(url)                 #Get该网页从而获取该html内容
    soup = BeautifulSoup(f.content, "lxml")  #用lxml解析器解析该网页的内容, 好像f.text也是返回的html
    content = soup.find_all('ul',class_="news-2" ) 
    #第二次解析内容
    hreflist=content[0].find_all("a")
    #print(hreflist)
    list1=[]
    list2=[]
    res=[]
    for k in hreflist:
        list1.append(k.get('href'))
        list2.append(k.string)
    res=zip(list1[:6],list2[:6])
    return res

###用户上传文件#######用户文件页#########删除文件#############################################
#用户上传文件
@login_required
def getfile(request):
    if request.method == 'POST':
        form = fileform(request.POST, request.FILES )  # 有文件上传要传两个字段
        f=request.FILES['file']
        #print(f.size)
        if form.is_valid():
            data=form.cleaned_data
            if request.session.get('username'):
                ext=data["file"].name.split(".")[-1].lower()
                if ext not in ["xls","xlsx","csv","xls","docx","doc","ppt","pptx","txt","rar","zip","jpg","jpeg","png","gif"]:
                    messages.success(request, '上传文件类型不支持！')
                    return render(request,'webforms.html', {'form': form}) #
                else:
                    if not  os.path.exists(os.path.join(settings.MEDIA_ROOT,request.session["username"])):
                        os.makedirs(os.path.join(settings.MEDIA_ROOT,request.session["username"]))
                    userfile.objects.create(
                        username= request.session["username"],
                        name=data["file"].name,
                        file=data["file"],
                        size=f.size
                    )
                    #print(username,name)
                    print(data["file"].size)
                    messages.success(request,data["file"].name+'上传成功')
            return render(request,'webforms.html', {'form': form}) #
        else:
            #print(form.errors)
            clean_errors=form.errors.get("__all__")
            #print(222,clean_errors)
        return render(request,"webforms.html",{"form":form,"clean_errors":clean_errors})
        
    else:
        #加载表单
        title="文件上传"
        form = fileform() 
        return render(request,'webforms.html', {'form': form,"title":title})

#用户文件
@login_required
def userfiles(request):    
    if request.session.get('username'):
        username= request.session["username"]
        newslist=getPage(request,userfile.objects.filter(username=username).order_by('-create_time'),8)
        return render(request, "userfiles.html",locals())
    else:
        return redirect("/logout/")

#删除文件
def delfile(request,fileid):
    if request.session.get('username'):
        username= request.session["username"]
        fobj=userfile.objects.filter(id=fileid).first()
        f=os.path.join(settings.MEDIA_ROOT,fobj.username,fobj.name)
        if os.path.exists(f) :
            os.remove(f)
        ret=userfile.objects.filter(id=fileid).delete()
    return redirect('/userfiles/')

################用户产品页######删除产品#######编辑产品######产品详细页######用户发布和修改产品######产品分类页##########
#普通用户产品页
#@login_required
def userproduct(request,typeid=0):    
    fbool=False
    
    #管理页面
    if typeid==0: 
        fbool=True
        if request.session.get('username'):
            username= request.session["username"]
            userobj=User.objects.get(username=username)
            newslist=getPage(request,product.objects.filter(user=userobj).order_by('-create_time'),8)
            return render(request, "userproduct.html",locals())
        else:
            return redirect("/logout/")
    else:
        #非管理页面
        fbool=False
        newslist=getPage(request,product.objects.filter(status="已审核").order_by('-create_time'),8)
        return render(request, "userproduct.html",locals())

#删除产品
def delproduct(request,productid):
    ret=product.objects.filter(id=productid).delete()
    return redirect('/userproduct/0')

#编辑产品
@csrf_exempt
@login_required
def editproduct(request,productid):
    productobj=product.objects.get(id=productid)
    context={
        'productid':productid,#内容id,传值到内容修改
        'productitem':productobj,
        'content_form':productform().as_p #调用发布和修改内容表单
    }
    if request.method=="GET":
        return render(request, 'editproduct.html', context=context)
    elif request.method=="POST":
        return  redirect('/userproduct/') #编辑成功后重定向到用户内容页

 #产品详细页
def productdetail(request,productid):    
    productobj=product.objects.get(id=productid)      
    request.session['id']=productid    
   
    if producthits.objects.filter(product=productobj):
       res = producthits.objects.update(num=F("num")+1)
    else:
        res=producthits.objects.create(
            product=productobj,
            num=1
        )   
    product_hitsobj=producthits.objects.filter(product=productobj).first()
    product_hits=product_hitsobj.num

    newslist=getPage(request,msgbook.objects.filter(product=productobj).order_by("-create_time"),10)
    return render(request, "productdetail.html", locals())

#普通用户发布和修改产品
@csrf_exempt
@login_required
def saveproduct(request):    
    #catelist=cate.objects.all()
    if request.method == 'POST':
        form = productform(request.POST,request.FILES )
        if form.is_valid():
            data=form.cleaned_data
            data["user"]=User.objects.get(username=request.user.username)
            productid=request.POST.get("productid") #接收修改内容的id，如果id存在，就修改，否则就新增内容
            if product.objects.filter(id=productid).exists():
                if not request.FILES:
                    data['img']=product.objects.filter(id=productid).first().img
                else:
                    data['ing']=request.FILES['img']
                #product.objects.filter(id=productid).update(**data)
                pobj=product.objects.get(id=productid)
                pobj.name=data["name"]
                pobj.cate=data["cate"]
                pobj.img=data['img']
                pobj.content=data['content']
                pobj.user=data['user']
                pobj.price=data['price']
                pobj.repository=data['repository']
                pobj.save()

                messages.success(request, '修改成功')
                #return redirect("/usernews/") #根据需要可重定向页面
            else:
                product.objects.get_or_create(**data)
                messages.success(request, '发布成功,等待审核')
            return render(request,'webforms.html', {'form': form}) #
        else:            
            #print(form.errors)
            clean_errors=form.errors.get("__all__")
            #print(222,clean_errors)
        return render(request,"webforms.html",{"form":form,"clean_errors":clean_errors})
    else:
        #加载表单
        title="产品发布与修改"
        form = productform() 
        return render(request,'webforms.html', {'form': form,'title':title})

#产品分类页
def pcate(request,cateid):
    cateobj=productcate.objects.get(id=cateid)
    newslist=getPage(request,product.objects.filter(cate=cateobj).order_by('-create_time'),6)
    return render(request, "productcate.html", locals())

########产品留言#########################################################################################
def signbook(request):  
    ipaddr=get_client_ip(request)
    id=request.session['id']
    productobj=product.objects.filter(id=id).first()
    if request.POST:
        msg=request.POST['s']
        #print(id,msg,request.user.username)
        #print(ret)
        if len(msg)>150:
            messages.success(request, '字数太多')
            return render(request,"signbook.html",locals())
        ret=txtaudit(msg)
        if ret in ["合规"]:
            if request.session.get('username'):
                username= request.session["username"]
                user=User.objects.get(username=request.user.username)
                ret=msgbook.objects.create(
                    user=user,
                    product=productobj,
                    msg=msg,
                    ipaddr=ipaddr,
                )
            
            else:
                ret=msgbook.objects.create(
                    product=productobj,
                    msg=msg,
                    ipaddr=ipaddr,
                )
            messages.success(request, '审核通过')
            return render(request,"signbook.html",locals())
        else:
            messages.success(request, '审核不通过')
            return render(request,"signbook.html",locals())
    else:
        return render(request,"signbook.html",locals())
####################################################################################################