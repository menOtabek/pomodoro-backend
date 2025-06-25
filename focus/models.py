from django.db import models
from django.utils.translation import gettext_lazy as _


class DurationCategory(models.Model):
    class DurationType(models.TextChoices):
        BREAK = 'break', _('Break')
        WORK = 'work', _('Work')

    type = models.CharField(max_length=10, choices=DurationType.choices, verbose_name=_('Duration'))
    minutes = models.PositiveIntegerField(_('Minutes'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = _('Duration')
        verbose_name_plural = _('Durations')


class PomodoroSession(models.Model):
    category = models.ForeignKey(DurationCategory, on_delete=models.CASCADE,
                                 verbose_name=_('Category'), related_name='pomodoro_sessions')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sessions', verbose_name=_('user'))
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=_('start time'))
    duration = models.PositiveIntegerField(_('Duration'), default=0)
    completed = models.BooleanField(default=True, verbose_name=_('completed'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def save(self, *args, **kwargs):
        self.completed = self.duration > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return _(f"{self.user} - {'Break' if self.is_break else 'Work'}")

    class Meta:
        verbose_name = _('Pomodoro Session')
        verbose_name_plural = _('Pomodoro Sessions')
