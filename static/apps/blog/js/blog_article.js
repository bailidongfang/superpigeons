$(document).ready(function () {
    //初始化emoji评论框
    $('#new_comment_textarea').emojioneArea();
    //显示emoji表情
    $('.comment_text_p').each(function () {
            var value = $(this).text();
            var code = $('<div/>').text(value).html(); //html转义
            $(this).html(emojione.toImage(code));
    })
    //评论提交
    $('#new_comment_btn').click(function () {
        if(jsdata.is_login=='false'){
            $('#infoModal h4').html('您还没有登陆，请先登录');
            $('#infoModal').modal('show');
            $('#infoModal').on('hide.bs.modal', function () {
                        window.location.href='/auth/login'
            })
            return false
        }
        if($('#new_comment_textarea').val()==''){
            $('#infoModal h4').html('内容为空');
            $('#infoModal').modal('show');
            return false
        }
        var post_json = {
            csrfmiddlewaretoken:jsdata.comment_csrf,
            comment_art_id:jsdata.comment_artid,
            comment_text:$('#new_comment_textarea').val(),
            commenter_id:jsdata.commenter_id,
        }
        $.post(jsdata.comment_url,post_json,function (response) {
            $('#infoModal h4').html('评论成功');
            $('#infoModal').modal('show');
            $('#infoModal').on('hide.bs.modal', function () {
                        window.location.reload()
            })
        })
    })
})