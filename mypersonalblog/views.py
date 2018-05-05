import math
import re
from datetime import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from mypersonalblog.templatetags.decoding import encrypt_password, enc, validate_password, dec
from .models import Article, SysUser, UserInfo, Articletag


# Create your views here.
def login(request):
    """
    跳转登录页面
    :param request:
    :return:
    """
    return render(request, 'login.html')


def login_required(func):
    """
    验证登陆的的装饰器
    :param func:
    :return:
    """
    def check_login(request, *args):
        if request.session.get('user_id', ''):
            user_id = request.session.get('user_id', '')
            userinfo = UserInfo.objects.get(userid=user_id)
        else:
            user_id = ''
            userinfo = ''
        return func(request, user_id, userinfo)

    return check_login


def is_upgrade(userid):
    """
    验证是否升级
    :param userid: 用户id
    :return:
    """
    user = UserInfo.objects.get(userid=userid)
    points = user.user_points
    if 100 <= points < 500:
        user.user_lv = math.floor(points / 100)
    else:
        user.user_lv += math.floor(points / 200)
    user.save()


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
    if user_id:
        is_upgrade(user_id)
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


def blog_det(request, art_id):
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
    is_upgrade(user_id)
    return render(request, 'usercenter.html', {'user_id': user_id, 'userinfo': userinfo})


@login_required
def modify_tel(request, user_id, userinfo):
    return render(request, 'modifytel.html', {'user_id': user_id, 'userinfo': userinfo})


@login_required
def modify_pwd(request, user_id, userinfo):
    return render(request, 'modifypwd.html', {'user_id': user_id, 'userinfo': userinfo})


@csrf_exempt
@login_required
def change_pwd(request, user_id, userinfo):
    oldpwd = request.POST['oldpwd']
    newpwd = request.POST['newpwd']
    renewpwd = request.POST['renewpwd']
    opassword = SysUser.objects.get(userid=user_id).password
    if not validate_password(enc(opassword), oldpwd):
        return HttpResponse('-1')
    elif newpwd != renewpwd:
        return HttpResponse('0')
    else:
        password = dec(encrypt_password(newpwd))
        data = SysUser.objects.get(userid=user_id)
        data.password = password
        data.save()
        return HttpResponse('1')


@login_required
def modify_email(request, user_id, userinfo):
    return render(request, 'modifyemail.html', {'user_id': user_id, 'userinfo': userinfo})


def writeblog(request, a_id):
    """
    渲染写博客页面
    :param request:
    :param a_id: 文章id
    :return:
    """
    if request.session.get('user_id', ''):
        user_id = request.session.get('user_id', '')
        userinfo = UserInfo.objects.get(userid=user_id)
    else:
        user_id = ''
        userinfo = ''
    tags = Articletag.objects.all()
    if a_id == '0':
        return render(request, 'writeblog.html', {'user_id': user_id, 'userinfo': userinfo, 'tags': tags})
    article = Article.objects.get(a_id=a_id)
    return render(request, 'writeblog.html', {'user_id': user_id, 'userinfo': userinfo, 'article': article,
                                              'tags': tags})


@csrf_exempt
def get_article(request):
    """
    新建和修改文章
    并将文章数据写入数据库
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
        try:
            a_id = request.POST['a_id']
            marticle = Article.objects.get(a_id=a_id)
            marticle.art_tit = title
            marticle.art_itr = introduction
            marticle.article_content = content
            marticle.type_no = art_typeno
            marticle.art_type = art_type
            marticle.article_tag = art_tag
            marticle.modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            marticle.save()
            return HttpResponse('1')
        except ValueError:
            userinfo = UserInfo.objects.get(userid=userid)
            userinfo.user_points += 10
            is_upgrade(userid)
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
    if request.method == 'GET':
        articles = Article.objects.all()
        pageinator = Paginator(articles, 5)
        try:
            page = request.GET.get('page')
            articles = pageinator.page(page)
        except PageNotAnInteger:
            articles = pageinator.page(1)
        except EmptyPage:
            articles = pageinator.page(pageinator.num_pages)
        return render(request, 'articlectrl.html', {'user_id': user_id, 'userinfo': userinfo, 'art_list': articles})


@csrf_exempt
def del_article(request):
    """
    文章删除
    :param request:
    :return:
    """
    a_id = request.POST['a_id']
    Article.objects.filter(a_id=a_id).delete()
    return HttpResponse('1')


@csrf_exempt
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
    if request.method == 'GET':
        articletags = Articletag.objects.all()
        pageinator = Paginator(articletags, 5)
        try:
            page = request.GET.get('page')
            tags = pageinator.page(page)
        except PageNotAnInteger:
            tags = pageinator.page(1)
        except EmptyPage:
            tags = pageinator.page(pageinator.num_pages)
        return render(request, 'tagctrl.html', {'user_id': user_id, 'userinfo': userinfo, 'tags': tags})
    elif request.method == 'POST':
        tagname = request.POST['tagname']
        data = Articletag(tagname=tagname)
        data.save()
        return HttpResponse('1')


@csrf_exempt
def del_tag(request):
    """
    删除标签
    :param request:
    :return:
    """
    t_id = request.POST['t_id']
    print(t_id)
    Articletag.objects.filter(t_id=t_id).delete()
    return HttpResponse('1')


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
    users = UserInfo.objects.all()
    pageinator = Paginator(users, 5)
    try:
        page = request.GET.get('page')
        userlist = pageinator.page(page)
    except PageNotAnInteger:
        userlist = pageinator.page(1)
    except EmptyPage:
        userlist = pageinator.page(pageinator.num_pages)
    return render(request, 'adminctrl.html', {'user_id': user_id, 'userinfo': userinfo, 'userlist': userlist})
# def showjokes(request):
#     day_joke = Joke()
#     jokes = day_joke.get_joke()
#     print(jokes)
#     return render(jokes, 'index.html', {'jokes': jokes})
