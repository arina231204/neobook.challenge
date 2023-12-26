# Generated by Django 3.2 on 2023-12-26 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_auto_20231224_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Нa расмотрении', 'PENDING'), ('Делается', 'APPROVED'), ('Доставлено', 'COMPLETED'), ('Отменено', 'CANCEL')], default='PENDING', max_length=20),
        ),
    ]
