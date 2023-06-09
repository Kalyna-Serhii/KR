# Generated by Django 4.1.7 on 2023-04-25 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0017_turn_status_alter_turn_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='all_service_time',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='turn',
            name='all_waiting',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='turn',
            name='expected_hours',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='turn',
            name='expected_minutes',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='turn',
            name='time_at_the_top',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='turn',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Статус черги'),
        ),
        migrations.AlterField(
            model_name='user',
            name='registration_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 4, 25, 11, 27, 28, 542799, tzinfo=datetime.timezone.utc)),
        ),
    ]
