"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import *
#from untitled import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve  # 导入相关静态文件处理的views控制包

from untitled import views
from untitled.settings import MEDIA_ROOT  # 导入项目文件夹中setting中的MEDIA_ROOT绝对路径

urlpatterns = [
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('blog/', include('blog.urls')),
    url('',views.home,name='主页'),
    path(r'mdeditor/', include('mdeditor.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
