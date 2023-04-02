# Generated by Django 4.1.7 on 2023-03-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0004_alter_user_user_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_number',
        ),
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]