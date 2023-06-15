# Generated by Django 4.2.1 on 2023-06-15 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiry', '0011_auto_20230614_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '03.  Educational Details',
            },
        ),
        migrations.RenameField(
            model_name='inquiry',
            old_name='address',
            new_name='guardian_name',
        ),
        migrations.RenameField(
            model_name='inquiry',
            old_name='education_qualification',
            new_name='permanent_address',
        ),
        migrations.RenameField(
            model_name='inquiry',
            old_name='source',
            new_name='temporary_address',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='closed_reason',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='description',
        ),
        migrations.RemoveField(
            model_name='inquiry',
            name='stage',
        ),
        migrations.AddField(
            model_name='inquiry',
            name='applied_before',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='applied_country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='applied_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='city',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='college',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='country',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='course',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='institution',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='intake',
            field=models.CharField(default=True, max_length=100),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='marital_status',
            field=models.CharField(default='Single', max_length=255),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='passed_year',
            field=models.PositiveIntegerField(default=True),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=True, max_digits=5),
        ),
        migrations.AddField(
            model_name='inquiry',
            name='remarks',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
