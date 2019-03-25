from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

# AbstractUserのusernameフィールドのみメールアドレス形式に変更
class User(AbstractUser):
    username = models.EmailField(_('email address'), unique=True)
