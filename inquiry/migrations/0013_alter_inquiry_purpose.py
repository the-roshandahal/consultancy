# Generated by Django 4.2.1 on 2023-06-15 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0012_educationaldetails_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='purpose',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, to='inquiry.purpose'),
        ),
    ]
