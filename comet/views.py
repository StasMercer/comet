from PIL import Image
from django.shortcuts import HttpResponse, render
from django.conf import settings


def show_img(request, folder, img_name):

    img_path = settings.MEDIA_ROOT + '\\'+folder+'\\' + img_name

    try:
        with open(img_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except IOError:
        return HttpResponse('file open error')

