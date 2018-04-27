import re
from datetime import datetime

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .decoding import encrypt_password, enc, validate_password, dec
from .models import Article, SysUser, UserInfo


# Create your views here.
def login(request):
    """
    跳转登录页面
    :param request:
    :return:
    """
    return render(request, 'login.html')


def login_required(func):
    def check_login(request):
        if request.session.get('user_id', ''):
            user_id = request.session.get('user_id', '')
            userinfo = UserInfo.objects.get(userid=user_id)
        else:
            user_id = ''
            userinfo = ''
        return func(request, user_id, userinfo)

    return check_login


@login_required
def index(request, user_id, userinfo):
    """
    首页页面并验证是否登录
    :param request:
    :param user_id: 用户id
    :param userinfo: 用户信息
    :return:
    """
    # day_joke = Joke()
    # jokes = day_joke.get_joke()
    artics = art_intr(request)[:5]
    for artic in artics:
        artic.article_content = re.sub(r'<[^>]+>|[ ]|&nbsp;|&gt;|&lt;', '', artic.article_content)
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
    if request.session.get('user_id', ''):
        user_id = request.session.get('user_id', '')
        userinfo = UserInfo.objects.get(userid=user_id)
    else:
        user_id = ''
        userinfo = ''
    articles = Article.objects.get(a_id=art_id)
    return render(request, 'blogdet.html', {'user_id': user_id, 'userinfo': userinfo, 'article': articles})


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
        reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if SysUser.objects.filter(username=username):
            return HttpResponse('-1')
        else:
            SysUser.objects.create(username=username, password=password)
            userid = SysUser.objects.get(username=username).userid
            user_points = 50
            UserInfo.objects.create(user_tel=phone, user_eml=email, username=username, user_gender=gender,
                                    userid=userid, user_points=user_points, user_lv=0, nickname=nickname,
                                    reg_time=reg_time)
            return HttpResponse('1')


@login_required
def usercenter(request, user_id, userinfo):
    """
    跳转用户中心并验证登录
    :param request:
    :param user_id: 用户
    :param userinfo: 用户信息
    :return:
    """
    return render(request, 'usercenter.html', {'user_id': user_id, 'userinfo': userinfo})


@login_required
def writeblog(request, user_id, userinfo):
    """
    渲染写博客页面
    :param request:
    :param user_id: 用户id
    :param userinfo: 用户信息
    :return:
    """
    return render(request, 'writeblog.html', {'user_id': user_id, 'userinfo': userinfo})


@csrf_exempt
def getarticle(request):
    """
    将文章数据写入数据库
    :param request:
    :return:
    """
    if request.method == 'POST':
        title = request.POST['title']
        introduction = request.POST['introduction']
        content = request.POST['content']
        userid = request.session.get('user_id', '')
        art_typeno = request.POST['articletypeno']
        art_type = request.POST['articletype']
        art_tag = request.POST['art_tag']
        article_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # UserInfo.objects.get(userid=userid).user_points + 10
        userinfo = UserInfo.objects.get(userid=userid)
        userinfo.user_points += 10
        newarticle = Article(userid=userid, art_tit=title, art_itr=introduction, type_no=art_typeno,
                             art_type=art_type, article_tag=art_tag, article_time=article_time,
                             article_content=content)
        newarticle.save()
        userinfo.save()
    return HttpResponse('1')


@login_required
def articlectrl(request, user_id, userinfo):
    """
    渲染文章管理界面
    :param request:
    :param user_id: 用户id
    :param userinfo: 用户信息
    :return:
    """
    articles = Article.objects.all()[:5]
    return render(request, 'articlectrl.html', {'user_id': user_id, 'userinfo': userinfo, 'articles': articles})


@login_required
def tagctrl(request, user_id, userinfo):
    """
    渲染标签管理界面
    完成标签的增加删除
    :param request:
    :param user_id: 用户id
    :param userinfo: 用户信息
    :return:
    """
    return render(request, 'tagctrl.html', {'user_id': user_id, 'userinfo': userinfo})


@login_required
def adminctrl(request, user_id, userinfo):
    """
    渲染权限管理界面
    实现对账户权限管理
    :param request:
    :param user_id: 用户id
    :param userinfo: 用户信息
    :return:
    """
    return render(request, 'adminctrl.html', {'user_id': user_id, 'userinfo': userinfo})
# def showjokes(request):
#     day_joke = Joke()
#     jokes = day_joke.get_joke()
#     print(jokes)
#     return render(jokes, 'index.html', {'jokes': jokes})
