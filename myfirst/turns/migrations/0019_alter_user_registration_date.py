# Generated by Django 4.1.7 on 2023-04-25 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0018_turn_all_service_time_turn_all_waiting_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='registration_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 4, 25, 11, 27, 34, 779845, tzinfo=datetime.timezone.utc)),
        ),
    ]
