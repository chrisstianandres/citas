# Generated by Django 3.1.7 on 2021-10-30 16:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0006_auto_20210919_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='envio_stock_dia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2021, 10, 30, 11, 55, 22, 305668), unique=True),
        ),
    ]
