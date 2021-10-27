from django.shortcuts import render, redirect

from blog.forms import AddBlogForm
from blog.models import Blog


def home(请求):
    t=请求.GET.get('t',-1)
    hotblog = Blog.objects.order_by('-viewnum')[0:20]
    if t == '1':
        hotblog = Blog.objects.order_by('-time')[0:20]
    return render(请求, 'home.html', { 'hotblog': hotblog,'t':t})