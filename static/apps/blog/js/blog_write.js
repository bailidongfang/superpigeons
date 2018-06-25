$(document).ready(function () {
    //多层modal更新z-index
    $(document).on('show.bs.modal', '.modal', function (event) {
            var zIndex = 1050 + (10 * $(".modal-backdrop").length);
            $(this).css('z-index', zIndex);
    });
    //icheck初始化
    $('.icheck_input').iCheck({
    checkboxClass: 'icheckbox_square-blue',
    radioClass: 'iradio_square-blue'
    });
    //提交博客按钮
    $("#submit_write").click(function () {
        var bt = $(this)
        //禁用按钮
        bt.prop('disabled', true);
        //判断内容是否为空
        if($('#title').val()==''){
            ShowDialogAlert('提示','标题为空')
            bt.prop('disabled',false);
            return false;
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
                    ShowDialogAlert('提示','提交成功',function () {
                        $(window).unbind('beforeunload');
                        window.location.href = "/blog"
                    })
                    }
                else {
                    ShowDialogAlert('提示',rst)

                }
            }
        });
    });
    //标签编辑按钮
    $('#tags_edit').click(function () {
        $('#tagsModal').modal('show')
    });

    //tag标签方法
    function tags_edit_func(type,name,id) {
        if(type=='add'){
            $('#tags_edit_div').append('<span class="tag label label-info" id="'+id+'" style="margin:5px 5px;display: inline-block">'+name+'<span class="glyphicon glyphicon-remove" style="margin-left: 10px;cursor: pointer;top: 3px"></span></span>')
        }
    }
    //标签编辑内容初始化
    $.each($('.tags_lable'),function () {
        let tag_name=$(this).children('span').html();
        let tag_id=$(this).children('div').children('input').val();
        tags_edit_func('add',tag_name,tag_id)
    });
    //tags删除post
    function delete_tag_post(delete_tag_id,delete_tag) {
        $.post(jsdata.tags_url,
            {csrfmiddlewaretoken:jsdata.csrf,
            type:'delete',
            tag_id:delete_tag_id
            },
            function (rst) {
                if(rst=='success'){
                    delete_tag.remove();
                }
                else {
                    ShowDialogAlert('服务器返回',rst)
                }
            }
        );
    }
    //tags删除
    $("#tags_edit_div").on('click',"span span",function () {
        var delete_tag = $(this).parent('span');
        ShowDialogSelect('确认','确认删除此标签吗?',function () {
            var delete_tag_id = delete_tag.attr('id');
            //判断tagid是否在used_tags数组中
            if($.inArray(delete_tag_id,jsdata.used_tag)>=0){
                ShowDialogSelect('确认','此标签已经在您其他的博客中使用,删除后将其他博客将会失去此标签',function () {
                    delete_tag_post(delete_tag_id,delete_tag)
                })
            }else{
                delete_tag_post(delete_tag_id,delete_tag)
            }
        })
    }
    );
    //tags新增
    $("#tags_edit_add").click(function () {
        var new_tag = $('#tags_edit_add_input').val();
        // alert(tags_edit.add)
        $.post(jsdata.tags_url,
               {csrfmiddlewaretoken:jsdata.csrf,
                type:'add',
                tag_name:new_tag
               },
               function (rst) {
                    $.each(rst,function (key,value) {
                        tags_edit_func('add',value,key)
                    })
               })
    });
    //edit提交
    $('#tags_edit_commit').click(function () {
        var url=window.location.pathname;
        $('#blog_tags').load(url+" #blog_tags",function () {
            $('#tagsModal').modal('hide');
            $('.icheck_input').iCheck({
            checkboxClass: 'icheckbox_square-blue',
            radioClass: 'iradio_square-blue'
            });
        });
    })
    //离开确认
    $(window).bind('beforeunload',function(){
        return '您输入的内容尚未保存，确定离开此页面吗？';
    });
})
