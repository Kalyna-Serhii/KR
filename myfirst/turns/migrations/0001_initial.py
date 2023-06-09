# Generated by Django 4.1.7 on 2023-03-12 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn_title', models.CharField(max_length=100, verbose_name='Назва черги')),
                ('turn_text', models.TextField(verbose_name='Опис черги')),
                ('create_date', models.DateTimeField(verbose_name='Дата створення черги')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100, verbose_name="Ім'я користувача")),
                ('user_number', models.CharField(max_length=10, verbose_name='Порядковий номер користувача')),
                ('registration_date', models.DateTimeField(verbose_name='Дата реєстрації користувача')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='turns.turn')),
            ],
        ),
    ]
