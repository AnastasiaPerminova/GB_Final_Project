# Generated by Django 3.0.5 on 2024-03-11 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0005_auto_20240309_2125'),
    ]


    operations = [
        migrations.AddField(
            model_name='result',
            name='success_percentage',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(choices=[('Вариант 1', 'Вариант 1'), ('Вариант 2', 'Вариант 2'), ('Вариант 3', 'Вариант 3'), ('Вариант 4', 'Вариант 4')], max_length=200),
        ),
    ]