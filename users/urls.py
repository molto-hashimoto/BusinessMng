from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

# namespace定義
# 以下urlのnameを使用する際にusers:(name)として使用する
app_name = 'users'

# URL設計
# 1.トップページへはログイン済でなければアクセスを禁止する。
# 2.トップページは仮。本実装では別アプリケーションで実装する。
# 3.未ログインの場合は、ログインページに飛ばす。
# 4.全ページ共通のナビバーを表示する。
# 5.ナビバーにログイン/ログアウト/メンバ新規追加/登録内容変更へのリンクを設置する。
# 6./listは登録メンバ確認用。
# 7.ログイン成功時、ユーザ名(メールアドレス)宛にログイン用URL付きメールを送信する。
# 8.メールのログインURLから飛んだ場合、ログイン状態でトップページが表示される。
urlpatterns = [
    path('', login_required(views.top.as_view()), name='top'),
    path('member/<token>/', views.member.as_view(), name='member'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout.as_view(), name='logout'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('update/', views.update.as_view(), name='update'),
    path('list/', views.list.as_view(), name='list'),
    path('sendComp/', views.sendComp.as_view(), name='sendComp'),
]