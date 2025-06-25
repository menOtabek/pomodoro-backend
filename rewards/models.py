from django.db import models
from django.utils.translation import gettext_lazy as _


class Medal(models.Model):
    MEDAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='medals', verbose_name=_('user'))
    type = models.CharField(max_length=10, choices=MEDAL_CHOICES, verbose_name=_('type'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return f'{self.user} - {self.type}'

    class Meta:
        verbose_name = _('Medal')
        verbose_name_plural = _('Medals')


class CoinTransaction(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='user_coins', verbose_name=_('user'))
    amount = models.IntegerField(verbose_name=_('amount'))
    reason = models.CharField(max_length=255, verbose_name=_('reason'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return f'{self.amount} {self.reason}'

    class Meta:
        verbose_name = _('Coin transaction')
        verbose_name_plural = _('Coin transactions')


class Leaderboard(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='leaderboard',
                                verbose_name=_('user'))
    score = models.PositiveIntegerField(default=0, verbose_name=_('score'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return f'{self.user} - {self.score}'

    class Meta:
        verbose_name = _('Leaderboard')
        verbose_name_plural = _('Leaderboards')
        ordering = ['score']
