"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from sc import views
from django.views.static import serve
from webapp.settings import MEDIA_ROOT

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login/',views.logIn,name='login'),
    path('logout/',views.logOut,name='logout'),
    path('register/',views.register,name='register'),
    path('check_code/',views.check_code,name='check_code'),
    path('newscate/<cateid>',views.newscate,name="newscate"),
    path('newsdetail/<newsid>',views.newsdetail,name="newsdetail"),
    path("addnews/",views.savenews,name="addnews"),
    path("search/",views.search,name="search"),
    path("imgdetect/<img>",views.imgdetect,name="imgdetect"),
    path("xlsform",views.xlsform,name="xlsform"),
    path("uploadxls/",views.uploadxls,name="uploadxls"),

]
