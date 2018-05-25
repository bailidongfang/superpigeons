$(document).ready(function () {
    $("#submit_write").click(function () {
        //禁用按钮
        $(this).prop('disabled', true);
        //判断内容是否为空
        if($('#title').val()==''){
            $('#errorModal h4').html('内容为空');
            $('#errorModal').modal('show');
            return false
        }
        //更新textarea数据
        CKEDITOR.instances['id_text'].updateElement();
        //数据提交
        $.ajax({
            url:jsdata.comment_url,
            type:'POST',
            data:$('#write_form').serialize(),
            cache:false,
            success: function (rst) {
                if (rst=='success'){
                    $('#infoModal h4').html('提交成功')
                    $('#infoModal').modal('show')
                    }
                else {
                    $('#infoModal h4').html(rst)
                    $('#infoModal').modal('show')
                }
            }
        });
    })
    //infomodal关闭后页面跳转
    $('#infoModal').on('hide.bs.modal', function () {
           window.location.href = "/blog"
    });
    //标签编辑按钮
    $('#tags_edit').click(function () {
        $('#tagsModal').modal('show')
    })

    $("#tags_edit_add").click(function () {
        $.post(jsdata.tags_url,{csrfmiddlewaretoken:jsdata.csrf,tag_name:$('#tags_edit_input').val()},function (rst) {
            rst.each(function (d) {
                alert(d)
            })
        })
    })

})