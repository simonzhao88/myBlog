from django.http import HttpResponse
from django.shortcuts import render

from .decoding import *
from .models import SysUser
from .models import UserInfo


# Create your views here.
def Login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def loginVerify(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = SysUser.objects.all()
        for user in users:

            if user.username == username and validate_password(enc(user.password), password):
                user_list = SysUser.objects.all()
                context = {'user_list': user_list}
                return HttpResponse('1')
        return HttpResponse('-1')
    else:
        return HttpResponse('0')
def registerVerify(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['tel']
        email = request.POST['email']
        gender = request.POST['gender']
        pwd = encrypt_password(password)
        password = dec(pwd)
        # try:
        if SysUser.objects.filter(username=username):
            print(SysUser.objects.filter(username=username))
            return HttpResponse('-1')
        else:
            SysUser.objects.create(username=username, password=password)
            UserInfo.objects.create(user_tel=phone, user_eml=email, username=username, user_gender=gender)
            return HttpResponse('1')
        # except:
        #     return HttpResponse('0')
