# Generated by Django 3.0 on 2021-06-06 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_remove_status_battery_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='BATTERY_Type_status',
            field=models.CharField(default='normal', max_length=255),
        ),
    ]