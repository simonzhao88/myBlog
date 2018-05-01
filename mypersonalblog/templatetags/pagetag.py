from django import template

from ..models import UserInfo

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
    point = points - lv * 100
    return points
