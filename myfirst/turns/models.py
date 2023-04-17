from django.db import models


class Turn(models.Model):
    creator = models.IntegerField('Хазяїн черги')
    turn_title = models.CharField('Назва черги', max_length=100)
    turn_text = models.TextField('Опис черги')
    create_date = models.DateTimeField('Дата створення черги', auto_now_add=True)
    status = models.BooleanField('Статус черги', default=True)

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
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Очікувач'
        verbose_name_plural = 'Очікувачі'
