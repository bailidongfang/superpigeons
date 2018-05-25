$(document).ready(function () {
    //删除博客
    $('.article_delete').click(function () {
        let delete_aiticle_id = $(this).attr('id')
        $('#selectModal h4').html('确定要删除此博客？');
        $('#selectModal').modal('show');
        $('#selectModal_yes').click(function () {
            $('#selectModal').modal('hide');
            $.post(jsdata.inter_url,{csrfmiddlewaretoken:jsdata.csrf,type:'delete',article_id:delete_aiticle_id},function (rst) {
                if(rst=='success'){
                    $('#infoModal h4').html('删除成功');
                    $('#infoModal').modal('show');
                    $('#infoModal').on('hide.bs.modal', function () {
                        window.location.reload()
                        $(this).unbind()
                    })
                }
                else {
                    $('#infoModal h4').html(rst);
                    $('#infoModal').modal('show');
                }
            })
            $(this).unbind()
        })
    })


    //编辑博客
    $('.article_edit').click(function () {
        let edit_aiticle_id = $(this).attr('id')
        $('#selectModal h4').html('确定要编辑此博客？');
        $('#selectModal').modal('show');
        $('#selectModal_yes').click(function () {
            $('#selectModal').modal('hide');
            window.location.href=jsdata.edit_url.replace('artid',edit_aiticle_id);
            $(this).unbind()
        })
    })

})