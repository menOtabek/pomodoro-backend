from django.db import models


class Medal(models.Model):
    MEDAL_CHOICES = [
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
    ]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=MEDAL_CHOICES)
    awarded_at = models.DateTimeField(auto_now_add=True)

class CoinTransaction(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    amount = models.IntegerField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class Leaderboard(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)  # based on Pomodoro count + medal bonus
