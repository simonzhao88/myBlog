from django.urls import path, re_path

from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('login/loginVerify/', views.loginVerify, name='loginVerify'),
    path('', views.index, name='index'),
    path('art_intr', views.art_intr, name='art_intr'),
    path('register/', views.register, name='register'),
    path('register/registerVerify/', views.registerVerify, name='registerVerify'),
    path('logout/', views.logout, name='logout'),
    re_path('blogdet/(\d+)/', views.blogdet, name='blogdet'),
    path('usercenter/myinfo', views.usercenter, name='usercenter'),
    path('usercenter/writeblog', views.writeblog, name='writeblog'),
]

app_name = 'mypersonalblog'
