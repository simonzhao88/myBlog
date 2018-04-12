$(document).ready(function() {
    $('#login').submit(
        function () {
            var username = $('#inputEmail').val();
            var password = $('#inputPassword').val();
            if (!username) {
                $('.loginError').html('用户名不符合规范').show();
                return false;
            }
            if (!password) {
                $('.loginError').html('密码不符合规范').show();
                return false;
            }
            $.ajaxSetup({
                data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
            });
            $.ajax({
                type: "POST",
                url: '/loginVerify/',
                data: {username: username, password: password},
                dataType: 'json',
                cache: false,
                success: function (data) {
                    if (data == 1) {
                        location.href = '';
                    }
                    if (data == -1 || data == 0) {
                        $('.loginError').html('用户名不存在或者用户名密码不匹配').show();
                    }
                },
                error: function () {
                    $('.loginError').html('请求失败，请刷新页面后重试').show();
                }
            });
            return false;
        });
})