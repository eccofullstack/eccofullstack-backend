# Generated by Django 5.1.6 on 2025-03-03 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paypal_order_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
