from django.shortcuts import render
import time

import re

import markdown
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from notifications.models import Notification
from notifications.signals import notify

from blog.forms import AddBlogForm, AddContentForm, AddinvitationForm

from blog.models import Blog

import operator
# 将md文本转换为纯文本作为博客说明
from user.models import MyUser

# Create your views here.
#去标签
def mdtotex(str1):
    cancertag = re.compile(r'<[^>]+>', re.S)  # 去标签
    str2 = cancertag.sub(' ', str1)
    str3 = str2.replace("&nbsp;",r" ")
    str4 = str3.replace( '&#160;',r' ')
    str5 = str4.replace( '&lt;',r'<',)
    str6 = str5.replace( '&#60;',r'<')
    str7 = str6.replace( '&gt;',r'>')
    str8 = str7.replace( '&#62;',r'>')
    str9 = str8.replace( "&amp;",r"&")
    str10 = str9.replace( '&#38;',r'&')
    str11 = str10.replace( '&quot;',r'"')
    str12 = str11.replace( '&#34;',r'"')
    str13 = str12.replace( '&apos;',r'’')
    str14 = str13.replace('&#39;',r'’', )
    return ' '.join(str14.split())
#写博客
def writeblog(请求):
    if(请求.user.is_authenticated==False):
        return redirect('user:登录')
    if(请求.method == 'POST'):
        #获取前端页面填写在md编译器的博客内容
        str1=请求.POST['id_博客内容-wmd-wrapper-html-code']
        #用来去除前端md编译器的标签
        bloginfo=mdtotex(str1)[0:200]+'......'
        blog=Blog.objects.create(bloguser=请求.user,
                            title=请求.POST['title'],
                            bloginfo=bloginfo,
                            blogtext=请求.POST['博客内容'],
                            viewnum=1)
        return redirect('user:登录')
    else:
        #返回博客表单，用于填写博客内容
        form=AddBlogForm()
        return render(请求, 'writeblog.html',{'form':form})

#博客详情
def detail(请求):
    message=请求.GET.get('message',0)
    blogid=请求.GET.get('blogid')
    blog=Blog.objects.get(pk=blogid)
    blog.viewnum=blog.viewnum+1
    blog.save()
    blogtext = markdown.markdown(blog.blogtext.replace("\r\n", '  \n'), extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    newbloglist=Blog.objects.filter(bloguser=blog.bloguser).order_by('-pk')[0:10]#该用户的最新文章
    return render(请求,'detailblog.html',{'message':message,'blog':blog,'blogtext':blogtext,'bloguser':blog.bloguser,'newbloglist':newbloglist,})
#删除博客
def deleteblog(请求):
    if (请求.user.is_authenticated == False):
        return redirect('user:登录')
    blogid=请求.GET.get('blogid')
    Blog.objects.get(pk=int(blogid),bloguser=请求.user).delete()
    return redirect('user:用户博客')
#修改博客
def updateblog(请求):
    if (请求.user.is_authenticated == False):
        return redirect('user:登录')
    if (请求.method == 'POST'):
        blogid=请求.POST['blogid']
        blog = Blog.objects.get(pk=blogid, bloguser=请求.user)
        str1 = 请求.POST['id_博客内容-wmd-wrapper-html-code']
        bloginfo = mdtotex(str1)
        blog.title=请求.POST['title']
        blog.bloginfo=bloginfo[0:200]+'......'
        blog.blogtext=请求.POST['博客内容']
        blog.save()
        return redirect('user:用户博客')
    else:
        blogid=请求.GET.get('blogid')
        blog=Blog.objects.get(pk=blogid,bloguser=请求.user)
        form = AddBlogForm(initial={'博客内容':blog.blogtext})
        return render(请求, 'updateblog.html', {'form': form,'blog':blog})
#搜索博客
def searchblog(请求):
    keyword=请求.GET.get('key')#获取关键词
    if(keyword==""):
        return redirect('主页')#判断关键词是否为空
    blogall=Blog.objects.order_by('-viewnum')
    bloglist=[]
    for blog in blogall:
        if(keyword in blog.title or keyword in blog.bloginfo): #查找符合条件的博客
            bloglist.append(blog)
    return render(请求,'seachblog.html',{'bloglist':bloglist,'keyword':keyword})