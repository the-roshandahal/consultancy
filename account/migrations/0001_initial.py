# Generated by Django 3.2 on 2023-06-19 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': '01. Role',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_finance', models.BooleanField(default=0)),
                ('read_finance', models.BooleanField(default=0)),
                ('update_finance', models.BooleanField(default=0)),
                ('delete_finance', models.BooleanField(default=0)),
                ('manage_finance', models.BooleanField(default=0)),
                ('manage_company', models.BooleanField(default=0)),
                ('create_account', models.BooleanField(default=0)),
                ('read_account', models.BooleanField(default=0)),
                ('update_account', models.BooleanField(default=0)),
                ('delete_account', models.BooleanField(default=0)),
                ('manage_account', models.BooleanField(default=0)),
                ('create_leads', models.BooleanField(default=0)),
                ('read_leads', models.BooleanField(default=0)),
                ('update_leads', models.BooleanField(default=0)),
                ('delete_leads', models.BooleanField(default=0)),
                ('manage_leads', models.BooleanField(default=0)),
                ('create_hrm', models.BooleanField(default=0)),
                ('read_hrm', models.BooleanField(default=0)),
                ('update_hrm', models.BooleanField(default=0)),
                ('delete_hrm', models.BooleanField(default=0)),
                ('manage_hrm', models.BooleanField(default=0)),
                ('create_course', models.BooleanField(default=0)),
                ('read_course', models.BooleanField(default=0)),
                ('update_course', models.BooleanField(default=0)),
                ('delete_course', models.BooleanField(default=0)),
                ('manage_course', models.BooleanField(default=0)),
                ('create_student', models.BooleanField(default=0)),
                ('read_student', models.BooleanField(default=0)),
                ('update_student', models.BooleanField(default=0)),
                ('delete_student', models.BooleanField(default=0)),
                ('manage_student', models.BooleanField(default=0)),
                ('create_inquiry', models.BooleanField(default=0)),
                ('read_inquiry', models.BooleanField(default=0)),
                ('update_inquiry', models.BooleanField(default=0)),
                ('delete_inquiry', models.BooleanField(default=0)),
                ('manage_inquiry', models.BooleanField(default=0)),
                ('role', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.role')),
            ],
            options={
                'verbose_name_plural': '02. Permissions',
            },
        ),
    ]
