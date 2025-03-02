# Generated by Django 5.0.1 on 2025-03-02 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_orderdetails_updated_by_orderpayment_updated_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled'), ('returned', 'Returned'), ('refunded', 'Refunded'), ('success', 'Success')], default='pending', max_length=20),
        ),
    ]
