# Generated by Django 4.1.7 on 2023-03-28 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0006_remove_user_user_name_user_first_name_user_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(default=1231, max_length=100, verbose_name="Ім'я користувача"),
            preserve_default=False,
        ),
    ]
