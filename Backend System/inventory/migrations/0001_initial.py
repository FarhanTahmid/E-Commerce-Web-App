# Generated by Django 5.0.1 on 2025-01-28 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Stock_Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_type', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Product Status',
            },
        ),
    ]
