# Generated by Django 3.2 on 2023-05-25 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0002_auto_20230524_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='payment_details',
        ),
    ]
