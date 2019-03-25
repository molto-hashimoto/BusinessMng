from django.contrib import admin
from .models import User

# adminサイトにUser情報を表示する
admin.site.register(User)
