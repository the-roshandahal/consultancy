# Generated by Django 4.2.1 on 2023-06-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0004_attendance_delete_deviceattendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
    ]