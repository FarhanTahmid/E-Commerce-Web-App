# Generated by Django 5.0.1 on 2025-01-27 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_remove_customeruser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeruser',
            name='email',
            field=models.EmailField(help_text="The user's unique email address.", max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='customeruser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Indicates whether the user account is active.'),
        ),
    ]
