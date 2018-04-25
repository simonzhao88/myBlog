from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .decoding import encrypt_password, enc, validate_password, dec
from .models import Article, SysUser, UserInfo, ArtInfo


# Create your views here.
def login(request):
    """
    跳转登录页面
    :param request:
    :return:
    """
    print(2141241)
    return render(request, 'login.html')


def index(request):
    """
    首页页面并验证是否登录
    :param request:
    :return:
    """
    # day_joke = Joke()
    # jokes = day_joke.get_joke()
    artics = art_intr(request)
    user_id = request.session.get('user_id', '')
    if user_id:
        userinfo = UserInfo.objects.get(userid=user_id)
    else:
        userinfo = 'null'
    return render(request, 'index.html', {'artics': artics, 'user_id': user_id, 'userinfo': userinfo})


def register(request):
    """
    跳转注册页面
    :param request:
    :return:
    """
    return render(request, 'register.html')


def art_intr(request):
    """
    从数据库获取文章数据
    :param request:
    :return:
    """
    return Article.objects.all()


def blogdet(request, art_id):
    """
    博客详情页面并验证是否登录
    :param request:
    :param art_id: 文章id
    :return:
    """
    user_id = request.session.get('user_id', '')
    artinfo = ArtInfo.objects.get(art_id=int(art_id))
    article = Article.objects.get(art_id=int(art_id))
    if user_id:
        userinfo = UserInfo.objects.get(userid=user_id)
    else:
        userinfo = 'null'
    return render(request, 'blogdet.html', {'user_id': user_id,
                                            'userinfo': userinfo,
                                            'artinfo': artinfo,
                                            'article': article, })


@csrf_exempt
def loginVerify(request):
    """
    登录验证
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = SysUser.objects.all()
        for user in users:
            if user.username == username and validate_password(enc(user.password), password):
                request.session['user_id'] = user.userid
                request.session.set_expiry(0)
                # user_list = SysUser.objects.all()
                # context = {'user_list': user_list}
                return HttpResponse(1)
        return HttpResponse(-1)
    else:
        return HttpResponse(0)


def logout(request):
    """
    安全退出，跳转首页
    :param request:
    :return:
    """
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponseRedirect('/')


def registerVerify(request):
    """
    注册验证并将数据写入数据库
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['tel']
        email = request.POST['email']
        gender = request.POST['gender']
        nickname = request.POST['nickname']
        pwd = encrypt_password(password)
        password = dec(pwd)
        if SysUser.objects.filter(username=username):
            return HttpResponse('-1')
        else:
            SysUser.objects.create(username=username, password=password)
            UserInfo.objects.create(user_tel=phone, user_eml=email, nickname=nickname, user_gender=gender)
            return HttpResponse('1')


def usercenter(request):
    """
    跳转用户中心并验证登录
    :param request:
    :return:
    """
    try:
        user_id = request.session.get('user_id', '')
        userinfo = UserInfo.objects.get(userid=user_id)
    except:
        user_id = ''
        userinfo = ''
        return render(request, 'usercenter.html', {'user_id': user_id, 'userinfo': userinfo})
    return render(request, 'usercenter.html', {'user_id': user_id, 'userinfo': userinfo})


def writeblog(request):
    """
    写博客页面
    :param request:
    :return:
    """
    user_id = request.session.get('user_id', '')
    userinfo = UserInfo.objects.get(userid=user_id)
    return render(request, 'writeblog.html', {'user_id': user_id, 'userinfo': userinfo})


def getarticle(request):
    """
    将文章数据写入数据库
    修改文章数据
    :param request:
    :return:
    """
    pass


def articlectrl(request):
    """
    渲染文章管理界面
    :param request:
    :return:
    """
    user_id = request.session.get('user_id', '')
    userinfo = UserInfo.objects.get(userid=user_id)
    return render(request, 'articlectrl.html', {'user_id': user_id, 'userinfo': userinfo})


def tagctrl(request):
    """
    渲染标签管理界面
    完成标签的增加删除
    :param request:
    :return:
    """
    user_id = request.session.get('user_id', '')
    userinfo = UserInfo.objects.get(userid=user_id)
    return render(request, 'tagctrl.html', {'user_id': user_id, 'userinfo': userinfo})


def adminctrl(request):
    """
    渲染权限管理界面
    实现对账户权限管理
    :param request:
    :return:
    """
    user_id = request.session.get('user_id', '')
    userinfo = UserInfo.objects.get(userid=user_id)
    return render(request, 'adminctrl.html', {'user_id': user_id, 'userinfo': userinfo})
# def showjokes(request):
#     day_joke = Joke()
#     jokes = day_joke.get_joke()
#     print(jokes)
#     return render(jokes, 'index.html', {'jokes': jokes})
