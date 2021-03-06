# Generated by Django 3.0.2 on 2020-03-02 23:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appProprietario', '0018_auto_20200226_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente_vaga',
            name='cliente',
            field=models.ForeignKey(default='', editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cliente_vaga',
            name='hora_entrada',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 3, 2, 23, 26, 48, 938569, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='cliente_vaga',
            name='vaga',
            field=models.ForeignKey(default='', editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Vaga', to='appProprietario.Vaga'),
        ),
    ]
