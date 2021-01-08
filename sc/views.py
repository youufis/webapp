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
from sc.addnews import newsform
from django.contrib import messages
import random
import socket
from django.db.models import Q
import pandas as pd
import threading
import shutil

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

#生成验证码
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

def logOut(request):
    try:
        logout(request)
    except Exception as e:
        print(e)
    return redirect(request.META['HTTP_REFERER'])

def logIn(request):
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
                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                # 重定向跳转
    return redirect(request.session['login_from'], '/')

##########################################    
#图像审核
def imgtoaudit():
    file_dir=os.path.join(settings.MEDIA_ROOT,"images")
    fname=random.sample(os.listdir(file_dir),4)    
    
    for img in fname:    
        fimg=auditimg.objects.filter(imgname=img)  #审核过的图像不用再审
        if not fimg.exists():   
            print(img)   
            if imgaudit(img) in ['合规']: #图像审核通过存入图像库
                #fname[fname.index(img)]="audit.jpg"
                ret=auditimg.objects.get_or_create(
                    imgname=img,
                    )
            else: #不合规移动回收站
                fsrc=os.path.join(settings.MEDIA_ROOT,"images",img)
                fdst=os.path.join(settings.MEDIA_ROOT,"recycle",img)
                shutil.move(fsrc,fdst)
            

#定义一个图象审核线程
def timgtoaudit():
    t = threading.Thread(target=imgtoaudit)       
    t.setDaemon(True)
    t.start()

#首页
def index(request):
    timgtoaudit() #开启线程进行图像审核
    fname=[]
    hostip=get_host_ip()
    clientip=get_client_ip(request)
    res=ipinfo.objects.create(
        ipaddr=clientip
    )
    hits=ipinfo.objects.all().count    
    fnameobj=auditimg.objects.all().order_by('?')[:3]    #图像库随机取4个
    for f in fnameobj:
        fname.append(f.imgname)
    #imgpath=(os.path.join(settings.MEDIA_ROOT,"images",f))
   

    catelist=cate.objects.all()
    newslist=[]
    for cateobj in catelist:        
        newslist.append(getPage(request,news.objects.filter(Q(cate=cateobj)&Q(status='已审核')).order_by("-create_time"),6))
    catenewslist=zip(catelist,newslist)
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

#内容类别页
def newscate(request,cateid):
    catelist=cate.objects.all()
    cateobj=cate.objects.get(id=cateid)
    newslist=getPage(request,news.objects.filter(cate=cateobj).order_by('-create_time'),6)
    return render(request, "cate.html", locals())

 #内容详细页
def newsdetail(request,newsid):    
    newsobj=news.objects.get(id=newsid)
    newshits.objects.create(
        news=newsobj
    )
    news_hits=newshits.objects.filter(news=newsobj).count
    return render(request, "newsdetail.html", locals())

#普通用户发布和修改内容
@csrf_exempt
@login_required
def savenews(request):    
    if request.method == 'POST':
        form = newsform(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            data["user"]=User.objects.get(username=request.user.username)
            newsid=request.POST.get("newsid") #接收修改内容的id，如果id存在，就修改，否则就新增内容
            if news.objects.filter(id=newsid).exists():
                news.objects.filter(id=newsid).update(**data)
                messages.success(request, '修改成功')
                #return redirect("/usernews/") #根据需要可重定向页面
            else:
                news.objects.get_or_create(**data)
                messages.success(request, '发布成功,等待审核')
            return render(request,'addnews.html', {'form': form}) #
        else:
            
            #print(form.errors)
            clean_errors=form.errors.get("__all__")
            #print(222,clean_errors)
        return render(request,"addnews.html",{"form":form,"clean_errors":clean_errors})
    else:
        #加载表单
        form = newsform() 
        return render(request,'addnews.html', {'form': form})
        
#标题搜索
def search(request):
    ctx ={}
    if request.POST:
        ctx['keywords'] = request.POST['q']
    res=ctx['keywords']
    newslist=getPage(request,news.objects.filter(title__contains= ctx['keywords']).order_by("-create_time"),10)
    return render(request,"result.html",locals())

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

#excel文件导入页
@login_required
def xlsform(request):
    return render(request,"uploadxls.html",locals())

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

    
   
    