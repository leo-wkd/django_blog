
from django.urls import path
from user import  views
app_name = 'user'
urlpatterns = [
    path('login',views.userlogin,name='登录'),
    path('register/',views.userregister,name='注册'),
    path('logout/', views.userlogout, name='登出'),
    path('updateuserinfo/',views.updateuserinfo,name='更改信息'),
    path('updatepassword/',views.updatepassword,name='修改密码'),
    path('userblog/',views.userblog,name='用户博客'),
]