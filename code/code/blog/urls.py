from django.urls import path,include
from . import  views
app_name = 'blog'
urlpatterns = [
    path('write/',views.writeblog,name='发表博客'),
    path('detail/',views.detail,name='博客详情'),
    path('delete/', views.deleteblog, name='删除博客'),
    path('update/', views.updateblog, name='修改博客'),
    path('searchblog/', views.searchblog, name='搜索博客'),
]
