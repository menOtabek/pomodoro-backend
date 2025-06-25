from django.db import models
from django.utils.translation import gettext_lazy as _


class MusicTrack(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    artist = models.CharField(max_length=200, verbose_name=_('artist'))
    audio_file = models.FileField(upload_to='music/', verbose_name=_('audio_file'))
    price = models.PositiveIntegerField(verbose_name=_('price in coins'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Music track')
        verbose_name_plural = _('Music tracks')


class PurchasedMusic(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='purchased_music',
                             verbose_name=_('user'))
    track = models.ForeignKey(MusicTrack, on_delete=models.CASCADE, related_name='purchased_music',
                              verbose_name=_('track'))
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name=_('purchased at'))

    def __str__(self):
        return self.track.name

    class Meta:
        verbose_name = _('Purchased music')
        verbose_name_plural = _('Purchased musics')
