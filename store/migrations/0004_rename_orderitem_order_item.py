# Generated by Django 4.0.4 on 2022-05-29 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='Order_item',
        ),
    ]