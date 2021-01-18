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
    path("uploadxls/",views.uploadxls,name="uploadxls"),
    path("usernews/",views.usernews,name="usernews"),
    path("delnews/<int:newsid>",views.delnews,name="delnews"),
    path("editnews/<int:newsid>",views.editnews,name="editnews"),
    path("getfile/",views.getfile,name="getfile"),
    path("userfiles/",views.userfiles,name="userfiles"),
    path("delfile/<int:fileid>",views.delfile,name="delfile"),
    path("userproduct/<int:typeid>",views.userproduct,name="userproduct"),
    path("delproduct/<int:productid>",views.delproduct,name="delproduct"),
    path("editproduct/<int:productid>",views.editproduct,name="editproduct"),
    path('productdetail/<int:productid>',views.productdetail,name="productdetail"),
    path('productcate/<cateid>',views.pcate,name="productcate"),
    path('addproduct/',views.saveproduct,name="addproduct"),
    path('signbook/',views.signbook,name="signbook"),
]
