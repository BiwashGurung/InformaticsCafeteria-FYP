# Generated by Django 5.1.5 on 2025-03-31 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteria', '0028_grouporder_grouporderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='group_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
