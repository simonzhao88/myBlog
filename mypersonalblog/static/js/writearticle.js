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
        var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        if (!title) {
            $('.error').html('请填写文章标题').show();
            return false;
        }
        if (!article_typeno) {
            $('.error').html('请选择文章类型').show();
            return false;
        }
        if (!art_tag) {
            $('.error').html('请选择文章标签').show();
            return false;
        }
        if (!introduction) {
            $('.error').html('请填写文章简介').show();
            return false;
        }
        if (!content) {
            $('.error').html('请填写文章内容').show();
            return false;
        }
        $.ajaxSetup({
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
        });
        $.ajax({
            type: "POST",
            url: 'getarticle',
            data: {
                title: title, introduction: introduction, content: content, articletypeno: article_typeno,
                articletype: article_type, csrf: csrftoken, art_tag: art_tag
            },
            dataType: 'json',
            cache: true,
            success: function (data) {
                if (data == 1) {
                    $('.error').html('提交成功!').show();
                }
                if (data == -1) {
                    $('.error').html('提交失败，请重试！').show();
                }
            },
            error: function () {
                $('.error').html('请求失败，请刷新页面后重试').show();
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