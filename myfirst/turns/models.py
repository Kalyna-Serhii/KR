from django.db import models
from django.utils import timezone


class Turn(models.Model):
    creator = models.IntegerField('Хазяїн черги')
    turn_title = models.CharField('Назва черги', max_length=100)
    turn_text = models.TextField('Опис черги')
    create_date = models.DateTimeField('Дата створення черги', auto_now_add=True)
    status = models.BooleanField('Статус черги', default=True)
    time_at_the_top = models.DateTimeField(null=True, blank=True)
    all_service_time = models.PositiveIntegerField(default=0)
    all_waiting = models.PositiveIntegerField(default=0)
    expected_hours = models.IntegerField(default=-1)
    expected_minutes = models.IntegerField(default=-1)

    def __str__(self):
        return self.turn_title

    class Meta:
        verbose_name = 'Черга'
        verbose_name_plural = 'Черги'


class User(models.Model):
    user_turn = models.ForeignKey(Turn, on_delete=models.CASCADE)
    username = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    registration_date = models.DateTimeField(timezone.now())

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Очікувач'
        verbose_name_plural = 'Очікувачі'
