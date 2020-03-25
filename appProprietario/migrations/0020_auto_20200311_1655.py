# Generated by Django 3.0.2 on 2020-03-11 19:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0019_auto_20200302_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaga',
            name='tipo_vaga',
            field=models.CharField(choices=[('n', 'Normal'), ('i', 'Idoso'), ('g', 'gestante'), ('d', 'deficiente')], default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cliente_vaga',
            name='hora_entrada',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 11, 19, 55, 32, 36941, tzinfo=utc)),
        ),
    ]