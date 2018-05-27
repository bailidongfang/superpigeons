$(document).ready(function () {
    //icheck
    $('.icheck_input').iCheck({
    checkboxClass: 'icheckbox_square-blue',
    radioClass: 'iradio_square-blue'
    });
    //tagsinput
    $('input#tags_edit_input').tagsinput({
      allowDuplicates: false,
      itemValue: 'id',
      itemText: 'name'
    });
    function tags_input() {
        $.each($('.tags_lable'),function () {
        let tag_name=$(this).children('span').html()
        let tag_id=$(this).children('div').children('input').val()
        $('input#tags_edit_input').tagsinput('add', {id:tag_id,name:tag_name});
        })
    }
    tags_input()
    $('input#tags_edit_input').on('beforeItemRemove', function(event) {
        var tag = event.item;
        // Do some processing here
        var tag_id = tag.id;
        var tag_name = tag.name
        // event.cancel = true
        $.each($('.tags_lable'),function () {
            if($(this).children('div').children('input').val()==tag_id){
                $(this).remove()
            }
        })

    });
    //提交博客按钮
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
        new_tag = $('#tags_edit_add_input')
        $('input#tags_edit_input').tagsinput('add', 'ff');
        // $.post(jsdata.tags_url,
        //        {csrfmiddlewaretoken:jsdata.csrf,
        //         tag_name:'dddd',
        //        },
        //        function (rst) {
        //             if(rst)
        //             $.each(rst,function (key,value) {
        //                 alert(key+':'+value)
        //             })
        //        })

    })

})