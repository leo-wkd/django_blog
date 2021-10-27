from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import MyUser
class MyUserChangeForm(UserChangeForm):  # 编辑用户表单重新定义，继承自UserChangeForm
    class Meta:
        model=MyUser
        fields=('username','password',)
class MyUserCreationForm(UserCreationForm):  # 创造用户表单重新定义，继承自UserCreationForm
    class Meta:
        model=MyUser
        fields=('name','username','password1')