# Generated by Django 3.0.2 on 2020-02-26 14:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0017_auto_20200226_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente_vaga',
            name='hora_entrada',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 2, 26, 14, 3, 51, 792648, tzinfo=utc)),
        ),
    ]
