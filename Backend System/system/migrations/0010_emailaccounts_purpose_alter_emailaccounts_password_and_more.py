# Generated by Django 5.0.1 on 2025-03-02 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0009_emailaccounts_emailtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailaccounts',
            name='purpose',
            field=models.CharField(choices=[('default', 'Default'), ('marketing', 'Marketing Emails'), ('transactional', 'Transactional Emails'), ('notification', 'Notification Emails'), ('support', 'Support Emails'), ('auth', 'Authentication'), ('no-reply', 'No Reply'), ('other', 'Other')], default='default', help_text='Email purpose', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emailaccounts',
            name='password',
            field=models.CharField(help_text='SMTP password (Use app password for gmail accounts!)', max_length=100),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='purpose',
            field=models.CharField(choices=[('default', 'Default'), ('marketing', 'Marketing Emails'), ('transactional', 'Transactional Emails'), ('notification', 'Notification Emails'), ('support', 'Support Emails'), ('auth', 'Authentication'), ('other', 'Other')], help_text='Template purpose', max_length=20),
        ),
    ]
