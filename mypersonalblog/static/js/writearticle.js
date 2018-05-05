$(function () {
    $('#commitarticle').click(function () {
        var title = $('#title').val();
        var introduction = $('#introduction').val();
        var content = $('#val').val();
        var article_typeno = $('#articletype').val();
        var article_type = $('#articletype').find('option:selected').text();
        var maxIndex = $('#tag a.tag').length - 1;
        var art_tag = '';
        $('#tag a.tag').text(function (index, content) {
            art_tag += (index === maxIndex) ? content : content + ',';
        });
        var a_id = $('#articleid').val();
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        if (!title) {
            $('.error').html('请填写文章标题').show(100).delay(5000).hide(100);
            return false;
        }
        if (!article_typeno) {
            $('.error').html('请选择文章类型').show(100).delay(5000).hide(100);
            return false;
        }
        if (!art_tag) {
            $('.error').html('请选择文章标签').show(100).delay(5000).hide(100);
            return false;
        }
        if (!introduction) {
            $('.error').html('请填写文章简介').show(100).delay(5000).hide(100);
            return false;
        }
        if (!content) {
            $('.error').html('请填写文章内容').show(100).delay(5000).hide(100);
            return false;
        }
        $.ajaxSetup({
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
        });
        $.ajax({
            type: "POST",
            url: '/usercenter/getarticle',
            data: {
                title: title, introduction: introduction, content: content, articletypeno: article_typeno,
                articletype: article_type, csrf: csrftoken, art_tag: art_tag, a_id: a_id
            },
            dataType: 'json',
            cache: true,
            success: function (data) {
                if (data == 1) {
                    $('.error').html('提交成功!').show(100).delay(5000).hide(100);
                }
                if (data == -1) {
                    $('.error').html('提交失败，请重试！').show(100).delay(5000).hide(100);
                }
            },
            error: function () {
                $('.error').html('请求失败，请刷新页面后重试').show(100).delay(5000).hide(100);
            }
        });
        return false;
    });
});
$(function () {
    $("#tag a").click(function () {
        $(this).toggleClass('tag');
    })
});
$(function () {
    if ($('#tpno').val()) {
        var typeno = $('#tpno').val();
        $('#articletype').val(typeno);
    }
});
$(function () {
    $('.del_art').click(function () {
        var result = window.confirm('您将要删除该文章，是否删除？');
        var a_id = $(this).attr("name");
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        if (result) {
            $.ajax({
                type: "POST",
                url: '/usercenter/del_article',
                data: {
                    a_id: a_id, csrf: csrftoken
                },
                dataType: 'json',
                cache: true,
                success: function (data) {
                    if (data == 1) {
                        $('.hint').html('删除成功!').show(100).delay(5000).hide(100);
                    }
                    if (data == -1) {
                        $('.hint').html('删除失败，请重试！').show(100).delay(5000).hide(100);
                    }
                },
                error: function () {
                    $('.hint').html('请求失败，请刷新页面后重试').show(100).delay(5000).hide(100);
                }
            });
        }
    })
});
$(function () {
    $('#tag_button').click(function () {
        $('#insert_tag').css('display', 'block');
    });
});
$(function () {
    $('.modifytag').click(function () {
        var tagname = $('.mtag').val();
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        if (!tagname) {
            $('.thint').html('请输入标签名!').show(100).delay(5000).hide(100);
            return false;
        }
        $.ajax({
            type: "POST",
            url: 'tagctrl',
            data: {
                tagname: tagname, csrf: csrftoken
            },
            dataType: 'json',
            cache: true,
            success: function (data) {
                if (data == 1) {
                    $('.thint').html('新增成功!').show(100).delay(5000).hide(100);
                    $('.mtag').val('');
                    $('.mtag').focus();
                }
                if (data == -1) {
                    $('.thint').html('新增失败，请重试！').show(100).delay(5000).hide(100);
                }
            },
            error: function () {
                $('.thint').html('请求失败，请刷新页面后重试').show(100).delay(5000).hide(100);
            }
        });
        return false;
    })
});
$(function () {
    $('.closem').click(function () {
        $('#insert_tag').css('display', 'none');
    });
});
$(function () {
    $('.del_tag').click(function () {
        var result = window.confirm('您将要删除该标签，是否删除？');
        var t_id = $(this).attr("name");
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        if (result) {
            $.ajax({
                type: "POST",
                url: 'del_tag',
                data: {
                    t_id: t_id, csrf: csrftoken
                },
                dataType: 'json',
                cache: true,
                success: function (data) {
                    if (data == 1) {
                        $('.thint').html('删除成功!').show(100).delay(5000).hide(100);
                    }
                    if (data == -1) {
                        $('.thint').html('删除失败，请重试！').show(100).delay(5000).hide(100);
                    }
                },
                error: function () {
                    $('.thint').html('请求失败，请刷新页面后重试').show(100).delay(5000).hide(100);
                }
            });
        }
    })
});
$(function () {
    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();

    function checknewpwd() {
        var newpwd = $('#newpwd').val();
        var pwdreg = /^\w{6,15}$/;
        if (pwdreg.test(newpwd)) {
            $('#newchangehint').text('√');
            $('#newchangehint').attr('class', 'correct');
            return true;
        } else {
            $('#newchangehint').text('X 密码长度为6-20');
            $('#newchangehint').attr('class', 'incorrect');
            return false;
        }
    }

    function checkrepwd() {
        var newpwd = $('#newpwd').val();
        var renewpwd = $('#rnewpwd').val();
        if (renewpwd == newpwd && renewpwd) {
            $('#rechangehint').text('√');
            $('#rechangehint').attr('class', 'correct');
            return true;
        } else {
            $('#rechangehint').text('X 两次输入的密码不一致');
            $('#rechangehint').attr('class', 'incorrect');
            return false;
        }
    }

    $('#newpwd').focus(function () {
        $('#newchangehint').text('');
        $('#newpwd').blur(checknewpwd);
    });
    //
    $('#rnewpwd').focus(function () {
        $('#rechangehint').text('');
        $('#rnewpwd').blur(checkrepwd);
    });

    $('.changepwd_cm').on('click', function (e) {
        var oldpwd = $('#oldpwd').val();
        var newpwd = $('#newpwd').val();
        var renewpwd = $('#rnewpwd').val();
        e = e || window.event;
        e.preventDefault();
        if (checkrepwd() & checknewpwd()) {
            $.ajax({
                type: "POST",
                url: 'change_pwd',
                data: {
                    oldpwd: oldpwd, newpwd: newpwd, renewpwd: renewpwd, csrf: csrftoken
                },
                dataType: 'json',
                cache: true,
                success: function (data) {
                    if (data == 1) {
                        $('.thint').html('修改密码成功!5秒后跳转登录页面！').show(100).delay(5000).hide(100);
                        setTimeout(function () {
                            location.href = '/login/'
                        }, 5000)
                    }
                    if (data == -1) {
                        $('.thint').html('原密码输入错误！请重试！').show(100).delay(5000).hide(100);
                    }
                    if (data == 0) {
                        $('.thint').html('两次输入密码不一致，请重新输入！').show(100).delay(5000).hide(100);
                    }
                },
                error: function () {
                    $('.thint').html('请求失败，请刷新页面后重试').show(100).delay(5000).hide(100);
                }
            });
        }

    });
});
$(function () {
    $('#mySwitch input').bootstrapSwitch({
        onText: '√',
        offText: 'X',
        size: 'large',
        onColor: 'info',
        offColor: 'info',
        onSwitchChange: function (e) {
            if (state == true) {
                alert(123);
            }
        }
    });
});