# Generated by Django 3.2 on 2023-05-28 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_quantity',
        ),
        migrations.RemoveField(
            model_name='course',
            name='course_type',
        ),
    ]