# Generated by Django 4.2.1 on 2023-06-02 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punch_in_time', models.TimeField()),
                ('punch_out_time', models.TimeField(blank=True, null=True)),
                ('tasks', models.TextField(blank=True, null=True)),
                ('meetings', models.TextField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrm.employee')),
            ],
            options={
                'verbose_name_plural': '01. Log Sheet',
            },
        ),
    ]
