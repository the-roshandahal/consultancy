# Generated by Django 3.2 on 2023-07-07 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='log_status',
        ),
    ]
