import datetime
from django.db import models
from django.utils import timezone


class Turn(models.Model):
    turn_title = models.CharField('Назва черги', max_length=100)
    turn_text = models.TextField('Опис черги')
    create_date = models.DateTimeField('Дата створення черги')

    def __str__(self):
        return self.turn_title

    # def was_create_recently(self):
    #     return self.create_date >= (timezone.now() - datetime.timedelta(days=7))

    class Meta:
        verbose_name = 'Черга'
        verbose_name_plural = 'Черги'


class User(models.Model):
    User = models.ForeignKey(Turn, on_delete=models.CASCADE, name="Зареєстрований у черзі")
    user_name = models.CharField("Ім'я користувача", max_length=100)
    # user_number = models.IntegerField('Порядковий номер користувача', default=0)
    position = models.PositiveIntegerField()
    registration_date = models.DateTimeField('Дата реєстрації користувача', auto_now_add=True)

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'Очікувач'
        verbose_name_plural = 'Очікувачі'
