$(document).ready(function () {
    var rst=$('#register_rst').text()
    if (rst=='success'){
        $('#registerModal h4').html('注册成功')
        $('#registerModal').modal('show')
    }
    if (rst=='error'){
        $('#registerModal h4').html('注册失败，联系管理员')
        $('#registerModal').modal('show')
    }

})