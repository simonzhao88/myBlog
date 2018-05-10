from django import template

from ..models import UserInfo, Article

register = template.Library()

from django.utils.html import format_html


@register.simple_tag
def circle_page(curr_page, loop_page):
    """
    自定义最多显示五页的分页标签
    :param curr_page:当前页
    :param loop_page:循环页（之前和之后）
    :return:
    """
    offset = abs(curr_page - loop_page)
    if offset < 5:
        if curr_page == loop_page:
            page_ele = '<li class="active"><a href="?page=%s">%s</a></li>' % (loop_page, loop_page)
        else:
            page_ele = '<li><a href="?page=%s">%s</a></li>' % (loop_page, loop_page)
        return format_html(page_ele)
    else:
        return ''


@register.simple_tag
def author(userid):
    """
    自定义作者标签
    :param userid:用户id
    :return:
    """
    authors = UserInfo.objects.get(userid=userid)
    nickname = authors.nickname
    return nickname


@register.simple_tag
def divi(points, lv):
    if 0 <= points < 500:
        point = points - lv * 100
    else:
        point = (points - lv * 100) / 2
    return point


@register.simple_tag
def enphone(phone):
    entel = phone.replace(phone[3:7], '*****')
    return entel


@register.simple_tag
def enemail(email):
    index = email.find('@')
    enmail = email.replace(email[index - 5:index], '****')
    return enmail


@register.filter
def next_page(aid):
    try:
        art = Article.objects.filter(a_id__gt=aid)
        return art[0].a_id
    except IndexError:
        return aid


@register.filter
def pre_page(aid):
    try:
        art = Article.objects.filter(a_id__lt=aid)
        return art[len(art) - 1].a_id
    except IndexError:
        return aid
    except AssertionError:
        return 1
