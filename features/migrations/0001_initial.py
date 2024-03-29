# Generated by Django 3.2 on 2023-07-10 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hrm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(max_length=255)),
                ('company_email', models.CharField(max_length=255)),
                ('company_contact_number', models.CharField(max_length=255)),
                ('company_logo', models.ImageField(upload_to='company_images/')),
                ('payment_terms', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '03. Company Setup',
            },
        ),
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('task_title', models.CharField(max_length=255)),
                ('task', models.TextField()),
                ('deadline', models.CharField(max_length=255)),
                ('task_from', models.CharField(max_length=255)),
                ('priority', models.CharField(max_length=255)),
                ('status', models.CharField(default='incomplete', max_length=255)),
                ('task_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrm.employee')),
            ],
            options={
                'verbose_name_plural': '02. To Do',
            },
        ),
    ]
