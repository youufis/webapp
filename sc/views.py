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
         
def index(request):

    hostip=get_host_ip()
    clientip=get_client_ip(request)
    res=ipinfo.objects.create(
        ipaddr=clientip
    )
    hits=ipinfo.objects.all().count    
    file_dir=os.path.join(settings.MEDIA_ROOT,"images")

    fname=random.sample(os.listdir(file_dir),4)
   
    #imgpath=(os.path.join(settings.MEDIA_ROOT,"images",f))


    catelist=cate.objects.all()
    newslist=[]
    for cateobj in catelist:        
        newslist.append(getPage(request,news.objects.filter(Q(cate=cateobj)&Q(status='已审核')).order_by("-create_time")))
    catenewslist=zip(catelist,newslist)
    return render(request,'index.html', locals())

def getPage(request, news_list):
    paginator = Paginator(news_list, 6)
    try:
        page = int(request.GET.get('page', 1))
        news_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        news_list = paginator.page(1)
    return news_list

def newscate(request,cateid):
    catelist=cate.objects.all()
    cateobj=cate.objects.get(id=cateid)
    newslist=getPage(request,news.objects.filter(cate=cateobj).order_by('-create_time'))
    return render(request, "cate.html", locals())
    
def newsdetail(request,newsid):    
    newsobj=news.objects.get(id=newsid)
    newshits.objects.create(
        news=newsobj
    )
    news_hits=newshits.objects.filter(news=newsobj).count
    return render(request, "newsdetail.html", locals())

@csrf_exempt
@login_required
def savenews(request):    
    if request.method == 'POST':
        form = newsform(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            data["user"]=User.objects.get(username=request.user.username)
            #print(data)
            news.objects.create(**data)
            messages.success(request, '发布成功,等待审核')
            return render(request,'addnews.html', {'form': form})
        else:
            
            #print(form.errors)
            clean_errors=form.errors.get("__all__")
            #print(222,clean_errors)
        return render(request,"addnews.html",{"form":form,"clean_errors":clean_errors})
    else:
        form = newsform()
        return render(request,'addnews.html', {'form': form})
        

def search(request):
    ctx ={}
    if request.POST:
        ctx['keywords'] = request.POST['q']
    res=ctx['keywords']
    newslist=getPage(request,news.objects.filter(title__contains= ctx['keywords']).order_by("-create_time"))
    return render(request,"result.html",locals())

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

@csrf_exempt
@login_required
def uploadxls(request):
    if request.method=="POST":
        f=request.FILES['file']
        filepath = os.path.join(settings.MEDIA_ROOT,"upfiles",f.name)
        ext=f.name.split(".")[-1].lower()
        if ext not in ["xls","xlsx","csv"]:
            return render(request,'uploadxls.html',{"error":"上传图像类型错误"})
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

@login_required
def xlsform(request):
    return render(request,"uploadxls.html",locals())

@login_required
def usernews(request):
    username= request.session["username"]
    userobj=User.objects.get(username=username)
    newslist=getPage(request,news.objects.filter(user=userobj).order_by('-create_time'))
    return render(request, "usernews.html",locals())

def delnews(request,newsid):
    ret=news.objects.filter(id=newsid).delete()
   
    return redirect('/usernews/')
   
    