# Generated by Django 3.2 on 2023-06-14 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20230528_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='create_inquiry',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='permission',
            name='delete_inquiry',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='permission',
            name='manage_inquiry',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='permission',
            name='read_inquiry',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='permission',
            name='update_inquiry',
            field=models.BooleanField(default=0),
        ),
    ]
