from django.db import models


class MusicTrack(models.Model):
    name = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='music/')
    price = models.PositiveIntegerField()  # in coins

class PurchasedMusic(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    track = models.ForeignKey(MusicTrack, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
