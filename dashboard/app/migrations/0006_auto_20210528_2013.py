# Generated by Django 3.0 on 2021-05-28 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210528_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='station_active',
            field=models.BooleanField(default=False),
        ),
    ]
