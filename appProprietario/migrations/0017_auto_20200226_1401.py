# Generated by Django 3.0.2 on 2020-02-26 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0016_auto_20200221_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente_vaga',
            name='hora_entrada',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 2, 26, 14, 1, 30, 854654)),
        ),
    ]
