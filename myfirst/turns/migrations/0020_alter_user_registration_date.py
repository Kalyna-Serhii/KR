# Generated by Django 4.1.7 on 2023-04-25 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0019_alter_user_registration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='registration_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 4, 25, 11, 27, 41, 803568, tzinfo=datetime.timezone.utc)),
        ),
    ]
