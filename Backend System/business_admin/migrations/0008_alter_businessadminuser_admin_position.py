# Generated by Django 5.0.1 on 2025-02-04 20:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_admin', '0007_alter_activitylog_activity_done_by_business_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessadminuser',
            name='admin_position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business_admin.adminpositions'),
        ),
    ]
