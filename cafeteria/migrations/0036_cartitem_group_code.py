# Generated by Django 5.1.5 on 2025-04-01 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteria', '0035_order_group_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='group_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
