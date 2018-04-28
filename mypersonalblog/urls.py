from django.urls import path, re_path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login/loginVerify/', views.loginVerify, name='loginVerify'),
    path('', views.index, name='index'),
    path('art_intr', views.art_intr, name='art_intr'),
    path('register/', views.register, name='register'),
    path('register/registerVerify/', views.registerVerify, name='registerVerify'),
    path('logout/', views.logout, name='logout'),
    re_path('blogdet/(\d+)/', views.blogdet, name='blogdet'),
    path('usercenter/myinfo', views.usercenter, name='usercenter'),
    re_path('usercenter/writeblog/(\d+)', views.writeblog, name='writeblog'),
    path('usercenter/articlectrl', views.articlectrl, name='articlectrl'),
    path('usercenter/tagctrl', views.tagctrl, name='tagctrl'),
    path('usercenter/adminctrl', views.adminctrl, name='adminctrl'),
    path('usercenter/getarticle', views.getarticle, name='getarticle'),
    # path('usercenter/modifyartic', views.modifyartic, name='modifyartic'),
]

app_name = 'mypersonalblog'
