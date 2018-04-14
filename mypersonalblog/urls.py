from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.Login, name='login'),
    path('login/loginVerify/', views.loginVerify, name='loginVerify'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/registerVerify/', views.registerVerify, name='registerVerify'),

]

app_name = 'mypersonalblog'
