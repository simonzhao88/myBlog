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