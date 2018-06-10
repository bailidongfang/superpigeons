$(document).ready(function () {
    //初始化emoji评论框
    $('#new_comment_textarea').emojioneArea();
    //显示emoji表情
    $('.comment_text_p').each(function () {
            var value = $(this).text();
            var code = $('<div/>').text(value).html(); //html转义
            $(this).html(emojione.toImage(code));
    });
    //初始化json
    var post_json = {
        csrfmiddlewaretoken:jsdata.comment_csrf,
        commenter_id:jsdata.commenter_id,
        comment_type:'',
        comment_art_id:'',
        comment_target:'',
        comment_text:''
    };
    //回复评论
    // $('.comments').on('click','.recomment',function () {
    // })
    $('.recomment').click(function () {
        //标题修改
        var headin_title = $('#new_comment .panel-heading .heading-title');
        var heading_text = $('#new_comment .panel-heading .heading-text');
        var comment_target_name = $('#commenter_name_'+$(this).attr('role')).html()
        headin_title.html("回复: "+comment_target_name);
        headin_title.css('margin-bottom','10px')
        heading_text.html('内容: '+$('#comment_text_p_'+$(this).attr('role')).html());
        heading_text.show()
        //滚动条到评论并获得焦点
        $('.emojionearea-editor').focus();
        $('body,html').animate({scrollTop:$('.emojionearea-editor').offset().top},100)
        //修改评论类型
        $('#new_comment_textarea').attr('type','com_comment');
        //修改postjson
        post_json.comment_target=$(this).attr('role')
    })
    //评论提交
    $('#new_comment_btn').click(function () {
        //判断登陆和内容为空
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
        //为postjson赋值
        post_json.comment_art_id=jsdata.comment_artid;
        post_json.comment_text=$('#new_comment_textarea').val();
        post_json.comment_type=$('#new_comment_textarea').attr('type');
        //post提交
        $.post(jsdata.comment_url,post_json,function (response) {
            if(response=='success'){
            $('#infoModal h4').html('评论成功');
            $('#infoModal').modal('show');
            $('#infoModal').on('hide.bs.modal', function () {
                        window.location.reload()
            })
            }
            else{
            $('#infoModal h4').html(response);
            $('#infoModal').modal('show');
            }
        })
    })
})