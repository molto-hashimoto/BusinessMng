
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm
)
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView
)
from django.contrib.auth import login as auth_login
from django.views import generic
from django.urls import reverse_lazy

# メール送信関連
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.shortcuts import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template
from django.conf import settings
from django.http import HttpResponseBadRequest

from .forms import signupForm, updateForm
from .models import User

# ログ設定
import logging
logger = logging.getLogger('command')

# 未ログインの場合、表示されない。
class top(generic.TemplateView):
    template_name = 'users/top.html'

class login(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/usr_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        # ボタンのテキスト内容
        context["button_text"] = "ログイン"
        # レイアウト設定
        context["layout"] = "col-md-6 offset-md-3"
        return context

    # ログイン成功時処理をオーバライドする。(メール送信機能を追加する。)
    def form_valid(self, form):
        # ログインしたユーザを取得
        user = form.get_user()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }
        # メール内容を作成
        subject_template = get_template('users/mail_template/subject.txt')
        subject = subject_template.render(context)
        message_template = get_template('users/mail_template/message.txt')
        message = message_template.render(context)
        # メール送信
        user.email_user(subject, message, from_email='mail_server@test.co.jp')

        ''' 以下、元のform_valid処理
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())
        '''
        return HttpResponseRedirect(reverse_lazy('users:sendComp'))

class member(generic.TemplateView):
    """メール内URLアクセス後のユーザーログイン"""
    template_name = 'users/top.html'
    # tokenの有効時間は30分とする(60秒*30)
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*30)

    def get(self, request, **kwargs):

        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()
        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()
        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except user.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                # すべて問題なければログインする
                auth_login(self.request, user)
                return super().get(request, **kwargs)

        return HttpResponseBadRequest()

class logout(LogoutView):
    template_name = 'users/logout.html'

class signup(generic.CreateView):
    form_class = signupForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/usr_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        # ボタンのテキスト内容
        context["button_text"] = "登録"
        # レイアウト設定
        context["layout"] = "col-md-6 offset-md-3"
        return context

class update(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/usr_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # はじめに継承元のメソッドを呼び出す
        # ボタンのテキスト内容
        context["button_text"] = "登録"
        # レイアウト設定
        context["layout"] = "col-md-6 offset-md-3"
        return context

class list(generic.ListView):
    model = User
    template_name = "users/list.html"

class sendComp(generic.TemplateView):
    template_name = 'users/send_comp.html'
