from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UserChangeForm
)
from .models import User

''' 未使用
class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる
'''

class signupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", )
        #field_classes = {'username': UsernameField}

    # saveをオーバーライドする
    # (ユーザ登録時にuserのemailにusername(メールアドレス)を入れる)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class updateForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'
        #field_classes = {'username': UsernameField}

