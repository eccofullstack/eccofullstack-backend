# Generated by Django 5.1.6 on 2025-03-01 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_price'),
        ('shopping_cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shoppingcartitem',
            unique_together={('cart', 'product')},
        ),
    ]
