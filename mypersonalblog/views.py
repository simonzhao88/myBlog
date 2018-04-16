from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .decoding import encrypt_password, enc, validate_password, dec
from .models import Article, SysUser, UserInfo


# Create your views here.
def Login(request):
    return render(request, 'login.html')

def index(request):
    artics = Article.objects.all()
    id = SysUser.objects.get(id=request.session['user_id'])
    return render(request, 'index.html', {'artics': artics, 'id': id})
    # return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')


def art_intr(request):
    print('1234567')
    artics = Article.objects.all()
    for artic in artics:
        print(artic)
    return render(request, 'index.html', {'artics': artics})


@csrf_exempt
def loginVerify(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = SysUser.objects.all()
        for user in users:

            if user.username == username and validate_password(enc(user.password), password):
                request.session['user_id'] = user.id
                print(request.session['user_id'])
                user_list = SysUser.objects.all()
                context = {'user_list': user_list}
                return HttpResponse('1')
        return HttpResponse('-1')
    else:
        return HttpResponse('0')


def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")



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
