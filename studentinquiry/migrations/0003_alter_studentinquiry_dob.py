# Generated by Django 3.2 on 2023-06-19 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentinquiry', '0002_auto_20230619_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinquiry',
            name='dob',
            field=models.CharField(max_length=255),
        ),
    ]