# Generated by Django 4.2.5 on 2023-11-20 20:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date_measured',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 20, 20, 49, 18, 348209), verbose_name='measured date'),
        ),
    ]
