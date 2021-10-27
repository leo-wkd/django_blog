from django import forms
from django.forms import Textarea
from mdeditor.fields import MDTextFormField
from blog.models import Blog
class AddBlogForm(forms.Form):
    博客内容=MDTextFormField(config_name='default')
class AddinvitationForm(forms.Form):
    博客内容=MDTextFormField(config_name='invitation')
class AddContentForm(forms.Form):
    评论=MDTextFormField(config_name='content')