# Generated by Django 3.0.5 on 2024-03-10 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_auto_20240311_0155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='email',
        ),
    ]