# Generated by Django 3.0 on 2021-05-29 09:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210529_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nozzle',
            name='vis_ip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Site'),
        ),
        migrations.AlterField(
            model_name='site',
            name='station_close_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 5, 29, 9, 47, 25, 34422), null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='station_open_time',
            field=models.TimeField(blank=True, default=datetime.datetime(2021, 5, 29, 9, 47, 25, 34422), null=True),
        ),
    ]
