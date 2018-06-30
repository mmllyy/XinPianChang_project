import hashlib
import uuid

import os

from XPC import settings
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from app.models import XpcUser
from app.models import Video


def newToken(userName):
    md5 = hashlib.md5()
    md5.update((str(uuid.uuid4())+userName).encode())
    return md5.hexdigest()


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    userName = request.POST.get('username')
    passwd = request.POST.get('passwd')
    qs = XpcUser.objects.filter(username=userName,userpasswd=crypt(passwd))
    print(qs)
    if qs.exists():
        user = qs.first()
        request.session['user_id'] = user.id
        user.token = newToken(user.username)
        user.save()
        resp = HttpResponseRedirect('/app/home')
        resp.set_cookie('token',user.token)
        return resp
    else:
        return render(request,'login.html',{'error_msg':'用户登录失败，请重试'})



def regist(request):
    if request.method == 'GET':
        return render(request,'register.html')
    print(request.FILES)
    print(request.POST.get('username'))
    print('头像:',request.FILES['img'])
    user = XpcUser()
    user.userName = request.POST.get('username')
    user.userPasswd = crypt(request.POST.get('passwd1'))
    uploadFile = request.FILES['img']
    print(user.img)
    saveFileName = newFileName(uploadFile.content_type)
    saveFilePath = os.path.join(settings.MEDIA_ROOT, saveFileName)
    with open(saveFilePath,'wb') as f:
        for part in uploadFile.chunks():
            f.write(part)
            f.flush()
    user.img = saveFilePath
    user.token = newToken(user.userName)
    user.save()
    resp = HttpResponseRedirect('/app/home')
    resp.set_cookie('token',user.token)
    return resp

def newFileName(contentType):
    fileName = crypt(str(uuid.uuid4()))
    extName = '.jpg'
    if contentType == 'image/png':
        extName  = '.png'
    return fileName + extName




def crypt(pwd,cryptName='md5'):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    return md5.hexdigest()


def home(request,num=1):
    if not request.COOKIES.get('token'):
        return HttpResponseRedirect('/app/login')
    #page_num = request.GET.get('page_num')
    print('页码:',num)
    videos = Video.objects.all()
    paginator = Paginator(videos,5)
    page = paginator.page(int(num))
    print(type(paginator.page_range))

    return render(request,'home_logined_collected.html',{'loginUser':XpcUser.objects.filter(token=request.COOKIES.get('token')).first(),
                                                         'current_page':num,
                                                         'movies':page.object_list,
                                                         'page_range':paginator.page_range
                                                         })


def modify(request):
    loginUser = request.GET.get('loginUser')
    return render(request,'userinfo_mod.html',{'loginUser':loginUser})