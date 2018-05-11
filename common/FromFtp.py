# URL：/media/通过FTP返回文件方法

import ftplib
from django.http import Http404
from django.http.response import FileResponse
from storages.backends.ftp import FTPStorage
import mimetypes


def get_from_ftp(request,path):
    storage = FTPStorage()
    if storage.exists(path):
        file = storage.open(path)
        content_type, encoding = mimetypes.guess_type(path)
        return FileResponse(file, content_type=content_type)
    else:
        raise Http404()


def headpic_to_ftp(path, content):
    storage = FTPStorage()
    if storage.exists(path):
        storage.delete(path)
        storage.save(path, content)
    else:
        storage.save(path, content)
