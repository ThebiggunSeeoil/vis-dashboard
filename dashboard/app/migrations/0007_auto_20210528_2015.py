# Generated by Django 3.0 on 2021-05-28 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210528_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='nozzle_mapping',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Nozzle'),
        ),
    ]