# Generated by Django 3.0 on 2021-06-15 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_persanaldetaillogin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persanaldetaillogin',
            name='key_login',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
    ]
