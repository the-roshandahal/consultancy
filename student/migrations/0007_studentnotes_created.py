# Generated by Django 4.1.4 on 2023-06-13 16:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20230613_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentnotes',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
