from django.http import JsonResponse
from django.shortcuts import render,redirect#redirect为重定向模块
from django.contrib.auth import authenticate,login,logout #从django.contrib.auth模块中导入用户验证，登录，登出模块
from django.urls import reverse
from notifications.models import Notification
from notifications.signals import notify

from blog.models import Blog
from user.models import MyUser
from . import admin#导入注册表单
from user.forms import MyUserChangeForm,MyUserCreationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm # admin中涉及到的两个表单
from user import models
# Create your views here.

#登出
def userlogout(请求):
    if 请求.user.is_authenticated:
        logout(请求)
    return render(请求, 'home.html')
#登录用户
def userlogin(请求):
    if 请求.method =='POST':
        user=authenticate(请求,username=请求.POST['username'],password=请求.POST['password'])#如果有该用户则返回该用户，没有则返回空
        if user is None:
            return render(请求,'login.html',{'erro':'密码错误或用户不存在！'})
        else:
            login(请求,user)
            return redirect('主页')
    elif 请求.user.is_authenticated:
        return redirect('主页')
    else:
        return render(请求, 'login.html')
#注册用户信息
def userregister(请求):
    if 请求.method=='POST':
        userForm=MyUserCreationForm(请求.POST)
        if userForm.is_valid():#判定注册用户表单是否合法
            userForm.save()
            #根据创建表单创建用户
            user = authenticate(username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password1'],name=userForm.cleaned_data['name'])
            login(请求,user)
            return redirect('主页')
    elif 请求.user.is_authenticated:
        return redirect('主页')
    else:
        userForm=MyUserCreationForm()
    #自定义注册错误信息
    FormErrorlist = []
    if('username' in userForm.errors):
        FormErrorlist.append('用户已注册')
    if ('password2' in userForm.errors):
        FormErrorlist.append('你的密码不能与其他个人信息太相似')
    return render(请求, 'userregister.html', {'FormErrorlist':FormErrorlist})

#更改个人信息
def updateuserinfo(请求):
    if 请求.user.is_authenticated==False:
        return redirect('主页')
    if 请求.method == 'POST':
        name=请求.POST.get('name')
        publicinfo=请求.POST.get('publicinfo')
        obj=MyUser.objects.get(id=请求.user.pk)
        obj.name=name
        obj.publicinfo = publicinfo
        obj.save()
        return redirect('主页')
    else:
        return redirect('主页')
#修改用户密码
def updatepassword(请求):
    if 请求.user.is_authenticated==False:
        return redirect('主页')
    if 请求.method == 'POST':
        newpassword = 请求.POST.get('newpassword')
        user = authenticate(请求, username=请求.user.username, password=请求.POST['oldpassword'])  #验证密码是否正确
        if(user is None):
            return render(请求, 'updatepassword.html',{'error':'请输入正确的旧密码'})
        请求.user.set_password(newpassword)
        请求.user.save()
        return redirect('主页')
    else:
        return render(请求,'updatepassword.html')

#用户博客列表
def userblog(请求):
    if 请求.user.is_authenticated==False:
        return redirect('user:登录')
    bloglist = Blog.objects.filter(bloguser=请求.user).order_by('-pk')  # 发布的博客
    return render(请求, 'userblog.html', {'bloglist': bloglist})