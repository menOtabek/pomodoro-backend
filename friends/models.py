from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests', verbose_name=_('From user'))
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests', verbose_name=_('To user'))
    accepted = models.BooleanField(default=False, verbose_name=_('Accepted'))
    rejected = models.BooleanField(default=False, verbose_name=_('Rejected'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    def __str__(self):
        return f"{self.from_user} ||| {self.to_user}"

    class Meta:
        unique_together = ['from_user', 'to_user']
        verbose_name = _('Friend request')
        verbose_name_plural = _('Friend requests')

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} || {self.friend}"

    class Meta:
        unique_together = ['user', 'friend']
        verbose_name = _('Friend request')
        verbose_name_plural = _('Friend requests')