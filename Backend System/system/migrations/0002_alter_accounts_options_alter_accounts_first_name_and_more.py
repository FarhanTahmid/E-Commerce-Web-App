# Generated by Django 5.0.1 on 2025-01-28 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accounts',
            options={'verbose_name': 'Account', 'verbose_name_plural': 'Accounts'},
        ),
        migrations.AlterField(
            model_name='accounts',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='middle_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Middle Name'),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='phone_no',
            field=models.CharField(blank=True, max_length=15, verbose_name='Phone Number'),
        ),
    ]
