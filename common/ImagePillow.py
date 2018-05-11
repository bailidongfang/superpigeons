from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def crop_image(file, left, top, right, buttom):
    # 打开图片
    im = Image.open(file)
    # 剪裁图片
    crop_im = im.crop((left, top, right, buttom))
    #设置背景颜色为白色
    # out = Image.new('RGBA', crop_im.size, (255,255,255))
    # out.paste(crop_im, (0, 0, 64, 64))
    # 保存图片
    image_io = BytesIO()
    crop_im.save(fp=image_io, format='JPEG')
    return ContentFile(image_io.getvalue())
