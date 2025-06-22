from django.db import models


class PomodoroSession(models.Model):
    class WorkDuration(models.IntegerChoices):
        TWENTY = 20, '20 minutes'
        TWENTY_FIVE = 25, '25 minutes'
        THIRTY = 30, '30 minutes'

    class BreakDuration(models.IntegerChoices):
        THREE = 3, '3 minutes'
        FIVE = 5, '5 minutes'
        SEVEN = 7, '7 minutes'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField()
    is_break = models.BooleanField(default=False)
    completed = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_break:
            valid_choices = [x.value for x in self.BreakDuration]
        else:
            valid_choices = [x.value for x in self.WorkDuration]

        if self.duration not in valid_choices:
            raise ValueError(f"Invalid duration {self.duration} for is_break={self.is_break}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{'Break' if self.is_break else 'Work'}: {self.duration} min"

    class Meta:
        verbose_name = 'Pomodoro Session'
        verbose_name_plural = 'Pomodoro Sessions'
