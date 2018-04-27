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
                preview: $(".avatar-preview").selector,
                crop: function (e) {
                    //返回图片编辑相关数据
                    $('#avatar_x').val(e.x);
                    $('#avatar_y').val(e.y);
                    $('#avatar_width').val(e.width);
                    $('#avatar_height').val(e.height);
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
                      alert('本地图片：可调整到最佳状态再上传');
                    } else {
                      alert('请选择一张图片');
                    }
                }
            }
        });

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