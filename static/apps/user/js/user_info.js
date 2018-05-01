$(document).ready(function () {
        //初始化裁剪器
        // function init() {
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
                    $('#avatar_x').val(e.detail.x);
                    $('#avatar_y').val(e.detail.y);
                    $('#avatar_width').val(e.detail.width);
                    $('#avatar_height').val(e.detail.height);
                },
            });
        // }


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
                $form.ajaxSubmit(function (headpicaddress) {
                        // $("#auther_info_headpic").attr('src','/outlib/'+headpicaddress)
                })
                // var formData = new FormData($("#avatar_form")[0]);
                //     $.ajax({
                //         url: jsdata.headpic_url,
                //         type: 'POST',
                //         data: formData,
                //         async: false,
                //         cache: false,
                //         contentType: false,
                //         processData: false,
                //         success: function (data){
                //             //更新导航右上角的头像
                //             $('.navbar-avatar').attr('src', '/' + data['avatar_url']);
                //             alert("上传头像成功");
                //         },
                //         error: function (err) {
                //             alert("提交失败，请重试！" + err);
                //         }
                //     });
        })

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

        //修改头像预览
        // $("#avatar-input").on('change',function () {
        //     var headpic=$(this)[0].files[0];
        //     var url=window.URL.createObjectURL(headpic)
        //     $("#avatar-wrapper img").attr('src',url)
        //     init()
        // })

})