$(document).ready(function () {
    $("#submit_write").click(function () {
        //禁用按钮
        $(this).prop('disabled', true);
        //更新textarea数据
        CKEDITOR.instances['id_text'].updateElement();
        //数据提交
        $.ajax({
            url:jsdata.comment_url,
            type:'POST',
            data:$('#write_form').serialize(),
            cache:false,
            success: function (rst) {
                $('#infoModal h4').html('提交成功')
                $('#infoModal').modal('show')
            }
        });
    })
    //模态框关闭后页面跳转
    $('#infoModal').on('hide.bs.modal', function () {
           window.location.href = "/blog"
   });
})