# Generated by Django 4.2.1 on 2023-06-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentinquiry', '0004_alter_studentinquiry_applied_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinquiry',
            name='closed_reason',
            field=models.CharField(default=True, max_length=255),
        ),
    ]