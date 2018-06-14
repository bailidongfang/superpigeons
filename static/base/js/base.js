function ShowDialogAlert(title,msg,func) {
        BootstrapDialog.alert({
            type:BootstrapDialog.TYPE_DEFAULT,
            size:BootstrapDialog.SIZE_SMALL,
            title: title,
            message:msg,
            closable: true,
            draggable : true,
            closeByBackdrop: false,
            closeByKeyboard: false,
            onhidden:func,
            buttons:[]
        })
};

function ShowDialogShow(title,msg,func) {
        BootstrapDialog.show({
            type:BootstrapDialog.TYPE_DEFAULT,
            size:BootstrapDialog.SIZE_SMALL,
            title: title,
            message:msg,
            closable: true,
            draggable : true,
            closeByBackdrop: false,
            closeByKeyboard: false,
            onhidden:func,
        })
};

function ShowDialogServerError(msg,func) {
        BootstrapDialog.alert({
            type:BootstrapDialog.TYPE_DEFAULT,
            size:BootstrapDialog.SIZE_SMALL,
            title: '服务器错误',
            message:msg,
            closable: true,
            draggable : true,
            closeByBackdrop: false,
            closeByKeyboard: false,
            onhidden:func
        })
};

function ShowDialogSelect(title,msg,funcok) {
        BootstrapDialog.show({
            type:BootstrapDialog.TYPE_DEFAULT,
            size:BootstrapDialog.SIZE_SMALL,
            title: title,
            message:msg,
            closable: true,
            draggable : true,
            closeByBackdrop: false,
            closeByKeyboard: false,
            buttons: [{
                label: '确定',
                cssClass:'btn btn-default btn-sm',
                action: function(dialog) {
                    funcok.call();
                    dialog.close()
                }
            }, {
                label: '取消',
                cssClass:'btn btn-default btn-sm',
                action: function(dialog) {
                    dialog.close()
                }
            }]
                });
}

