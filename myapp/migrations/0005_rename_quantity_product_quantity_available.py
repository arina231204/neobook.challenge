# Generated by Django 5.0 on 2023-12-17 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_cartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quantity',
            new_name='quantity_available',
        ),
    ]
