# Generated by Django 3.2 on 2023-07-19 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='log',
            field=models.BooleanField(default=True),
        ),
    ]
