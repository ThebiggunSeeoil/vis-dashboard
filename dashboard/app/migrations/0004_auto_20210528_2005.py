# Generated by Django 3.0 on 2021-05-28 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210528_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='station_active',
            field=models.CharField(default='False', max_length=255),
        ),
    ]
