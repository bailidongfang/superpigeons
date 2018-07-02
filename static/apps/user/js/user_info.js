$(document).ready(function () {
        //提交个人信息
        $('#user_info_submit').click(function () {
            $('#info_permission_name').val(jsdata.username);
            $.ajax({
                url:jsdata.userinfo_url,
                type:'POST',
                data:$('#user_info_form').serialize(),
                cache:false,
                success: function (rst) {
                    if (rst=='success'){
                        ShowDialogShow('提示','提交成功',function () {
                            window.location.href='/auth/userindex/'+jsdata.user
                        })
                        }
                    else {
                        ShowDialogAlert('提示',rst)
                    }
                }
            });
        })

        //初始化裁剪器
        var image = $('#avatar-wrapper img');
        image.cropper({
            checkImageOrigin: true, //检查图片来源
            dragMode: 'move',   //图片可移动
            restore:false,      //窗体调整大小之后不自动恢复裁剪区域
            zoomOnWheel: false, //不允许通过鼠标滚轮缩放
            zoomOnTouch: false, //不允许通过触摸缩放
            aspectRatio: 1 / 1, //裁剪比例
            autoCropArea: 0.5,  //裁剪背景透明度
            autoCropArea: 1,    //自动裁剪的比例

            //文本的jQuery选择表达式，一个div
            preview: ".avatar-preview",//预览区域
            crop: function (e) {
                //返回图片编辑相关数据
                $('#headpic_permission_name').val(jsdata.username);
                $('#avatar_x').val(e.detail.x);
                $('#avatar_y').val(e.detail.y);
                $('#avatar_width').val(e.detail.width);
                $('#avatar_height').val(e.detail.height);
            },
        });
        //上传图片事件
        $("#avatar-input").change(function(){
            var URL = window.URL || window.webkitURL;
            if(URL){
                var files = this.files;
                if (files && files.length){
                    var file = files[0];
                    if (/^image\/\w+$/.test(file.type)) {
                      var blobURL = URL.createObjectURL(file);
                      image.cropper('reset').cropper('replace', blobURL);
                      $('.avatar_crop .disabled').removeClass('disabled');
                    } else {
                      alert('请选择一张图片');
                    }
                }
            }
        });
        //上传按钮
        $('#upload').click(function () {
                if($('#avatar-wrapper img').attr('src')==''){
                        $('#infoModal h4').html('请先选择一个图片')
                        $('#infoModal').modal('show')
                        return false;}
                var $form=$("#avatar_form")
                $form.ajaxSubmit(function (rst) {
                        if (rst=='success'){
                            $('#infoModal h4').html('上传成功')
                            $('#infoModal').modal('show')
                            $('#infoModal').on('hide.bs.modal', function () {
                            window.location.reload()
                            $(this).unbind()
                            })
                        }
                        else {
                            $('#infoModal h4').html(rst)
                            $('#infoModal').modal('show')
                        }
                        // $("#auther_info_headpic").attr('src','/outlib/'+headpicaddress)
                })
        })
        //放大放小按钮
        var zoom = 1;
        $("#zoom-in").click(function(){
            if(zoom<1.5){
                zoom += 0.1;
                image.cropper("zoom", 0.1);
            }
        });
        $("#zoom-out").click(function(){
            if(zoom>0.5){
                zoom -= 0.1;
                image.cropper("zoom", -0.1);
            }
        });
        //复位按钮
        $('#reset').click(function(){
            image.cropper("reset");
            zoom = 1;
        });
        //bootstrap tab
        $('#left_nav a').click(function (e) {
            e.preventDefault()
            $(this).tab('show')
        })
})