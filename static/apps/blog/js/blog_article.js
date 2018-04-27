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
        var post_json = {
            csrfmiddlewaretoken:jsdata.comment_csrf,
            comment_art_id:jsdata.comment_artid,
            comment_text:$('#new_comment_textarea').val(),
            commenter_id:jsdata.commenter_id,
        }
        $.post(jsdata.comment_url,post_json,function (response) {
            alert(response)
        })
    })
})