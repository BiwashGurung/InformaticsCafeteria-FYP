# Generated by Django 5.1.5 on 2025-04-24 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteria', '0051_remove_order_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='scheduled_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
