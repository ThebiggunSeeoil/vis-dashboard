# Generated by Django 3.0 on 2021-05-28 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nozzle',
            name='log_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='nozzle',
            name='nozzle_num',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='nozzle',
            name='nozzle_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]