# Generated by Django 4.1.7 on 2023-04-02 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turns', '0011_turn_creator_alter_turn_turn_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turn',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата створення черги'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='creator',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='turn',
            name='turn_text',
            field=models.TextField(verbose_name='Опис черги'),
        ),
        migrations.AlterField(
            model_name='turn',
            name='turn_title',
            field=models.CharField(max_length=100, verbose_name='Назва черги'),
        ),
    ]
