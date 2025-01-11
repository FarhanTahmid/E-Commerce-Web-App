# Generated by Django 5.0.1 on 2025-01-11 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_colors_product_flavours_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed_amount', 'Fixed Amount')], max_length=30)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('isActive', models.BooleanField(default=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='products.product')),
            ],
            options={
                'verbose_name': 'Product Discount',
                'verbose_name_plural': 'Product Discounts',
            },
        ),
    ]
