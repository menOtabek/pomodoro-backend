from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_('email'))
    coins = models.PositiveIntegerField(default=0, verbose_name=_('coins'))
    picture = models.ImageField(upload_to='users/pictures', default='users/pictures/image.png', verbose_name=_('picture'))
    language = models.CharField(max_length=20, default='en', verbose_name=_('language'))
    first_name = models.CharField(max_length=55, verbose_name=_('first name'), blank=True, null=True)
    last_name = models.CharField(max_length=55, verbose_name=_('last name'), blank=True, null=True)
    username = models.CharField(max_length=55, unique=True, verbose_name=_('username'))
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name or ""} {self.last_name or ""}'.strip()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class OTP(models.Model):
    email = models.EmailField(verbose_name=_('email'))
    code = models.CharField(max_length=6, verbose_name=_('code'))
    otp_key = models.CharField(max_length=32, verbose_name=_('otp key'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    is_verified = models.BooleanField(default=False, verbose_name=_('is verified'))

    def __str__(self):
        return f"{self.email} - {self.code}"

    class Meta:
        verbose_name = _('OTP')
        verbose_name_plural = _('OTPs')
