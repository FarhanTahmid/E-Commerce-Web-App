# Generated by Django 5.0.1 on 2025-01-28 11:10

import django_resized.forms
import system.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email Address')),
                ('username', models.CharField(max_length=50, verbose_name='Username')),
                ('first_name', models.CharField(max_length=50, verbose_name='Full name')),
                ('middle_name', models.CharField(max_length=50, verbose_name='Middle name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name')),
                ('phone_no', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('profile_picture', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[244, 244], upload_to=system.models.get_customer_avatar_path)),
                ('skinType', models.CharField(blank=True, choices=[('normal', 'Normal'), ('oily', 'Oily'), ('dry', 'Dry'), ('combination', 'Combination'), ('sensitive', 'Sensitive')], max_length=20, verbose_name='Skin Type')),
                ('block', models.BooleanField(default=False, verbose_name='Block Account')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last Login')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ErrorLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('error_type', models.CharField(blank=True, max_length=255, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Error Log',
                'verbose_name_plural': 'Error Logs',
                'ordering': ['-timestamp'],
            },
        ),
    ]
