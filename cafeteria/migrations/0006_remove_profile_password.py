# Generated by Django 5.1.5 on 2025-01-27 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteria', '0005_alter_profile_email_alter_profile_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='password',
        ),
    ]
