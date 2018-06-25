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
        comment_tree:'',
        comment_text:''
    };
    //回复评论

    $('.recomment').click(function () {
        //标题修改
        var headin_title = $('#new_comment .panel-heading .heading-title');
        var heading_text = $('#new_comment .panel-heading .heading-text');
        var comment_target_name = $('#commenter_name_'+$(this).attr('role')).html();
        headin_title.html("回复: "+comment_target_name);
        headin_title.css('margin-bottom','10px')
        heading_text.html('内容: '+$('#comment_text_p_'+$(this).attr('role')).html());
        heading_text.show()
        //滚动条到评论并获得焦点
        $('.emojionearea-editor').focus();
        $('body,html').animate({scrollTop:$('.emojionearea-editor').offset().top},100);
        //修改评论类型
        $('#new_comment_textarea').attr('type','com_comment');
        //修改postjson
        post_json.comment_target=$(this).attr('role')
        post_json.comment_tree=$(this).attr('tree')
    })
    //评论提交
    $('#new_comment_btn').click(function () {
        var subbtn = $(this);
        subbtn.prop('disabled',true);
        //判断登陆和内容为空
        if(jsdata.is_login=='false'){
            ShowDialogShow('提示','您还没有登陆，请先登录',function () {
                window.location.href='/auth/login'
            });
            subbtn.prop('disabled',false);
            return false
        }
        if($('#new_comment_textarea').val()==''){
            ShowDialogAlert('提示','评论内存为空');
            subbtn.prop('disabled',false);
            return false
        }
        //为postjson赋值
        post_json.comment_art_id=jsdata.comment_artid;
        post_json.comment_text=$('#new_comment_textarea').val();
        post_json.comment_type=$('#new_comment_textarea').attr('type');
        //post提交
        $.post(jsdata.comment_url,post_json,function (response) {
            if(response.indexOf('success')!= -1){
                ShowDialogAlert('提示','评论成功',function () {
                    response.slice(7)
                    window.location.href='?cmd='+response.slice(7)
                })
            }
            else{
                ShowDialogServerError(response);
                subbtn.prop('disabled',false)
            }
        })
    });


    //获取url参数
    $.getUrlParam = function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]); return null;
    };
    //根据参数定位高度
    window.onload=function () {
        var id=$.getUrlParam('cmd')
        if(id != null){
        $('body,html').animate({scrollTop:$('#comment_text_p_'+id).offset().top-300},100);}
    }

})