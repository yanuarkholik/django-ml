# Generated by Django 4.1.2 on 2022-10-16 05:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_forecast_date_end_alter_forecast_date_st'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='date_end',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='date_st',
            field=models.DateField(default=datetime.datetime(2019, 10, 17, 12, 7, 22, 39603)),
        ),
    ]