# Generated by Django 2.0 on 2018-05-03 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Residencial', '0006_auto_20180427_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='fecha',
            field=models.DateField(auto_now_add=True, verbose_name='Fecha'),
        ),
    ]
