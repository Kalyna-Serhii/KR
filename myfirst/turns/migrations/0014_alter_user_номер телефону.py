# Generated by Django 4.1.7 on 2023-04-08 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0013_alter_turn_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Номер телефону',
            field=models.CharField(max_length=15),
        ),
    ]
