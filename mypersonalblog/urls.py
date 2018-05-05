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
    re_path('blogdet/(\d+)/', views.blog_det, name='blogdet'),
    path('usercenter/myinfo', views.usercenter, name='usercenter'),
    path('usercenter/myinfo/modifytel', views.modify_tel, name='modify_tel'),
    path('usercenter/myinfo/modifypwd', views.modify_pwd, name='modify_pwd'),
    path('usercenter/myinfo/changepwd', views.change_pwd, name='change_pwd'),
    path('usercenter/myinfo/modifyemail', views.modify_email, name='modify_email'),
    re_path('usercenter/writeblog/(\d+)', views.writeblog, name='writeblog'),
    re_path('usercenter/articlectrl/(\?page=\d+)', views.articlectrl, name='articlectrl'),
    path('usercenter/tagctrl', views.tagctrl, name='tagctrl'),
    path('usercenter/adminctrl', views.adminctrl, name='adminctrl'),
    path('usercenter/getarticle', views.get_article, name='getarticle'),
    path('usercenter/del_article', views.del_article, name='del_article'),
    path('usercenter/del_tag', views.del_tag, name='del_tag'),
]

app_name = 'mypersonalblog'
