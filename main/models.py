from config import settings
from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='пользователь')
    place = models.CharField(max_length=50, verbose_name='место')
    hours = models.IntegerField(verbose_name='часы')      # поля hours и minutes нужны для более удобного
    minutes = models.IntegerField(verbose_name='минуты')  # ввода времени пользователем
    time = models.TimeField(verbose_name='время', null=True, blank=True)
    action = models.CharField(max_length=60, verbose_name='действие')
    is_pleasant_habit = models.BooleanField(verbose_name='признак приятной привычки')
    connected_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                        verbose_name='связанная привычка')
    period = models.CharField(max_length=30, default="1D",
                              verbose_name='периодичность')
    reward = models.CharField(max_length=30, null=True, blank=True, verbose_name='вознаграждение')
    duration = models.IntegerField(verbose_name='продолжительность')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f"Я буду {self.action} в {self.hours} часов {self.minutes} минут в {self.place}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
