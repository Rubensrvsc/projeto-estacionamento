# Generated by Django 2.1.3 on 2019-10-18 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0005_cliente_vaga'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='usuario_cli',
        ),
        migrations.AlterField(
            model_name='proprietario',
            name='usuario_prop',
            field=models.OneToOneField(default='', editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prop', to=settings.AUTH_USER_MODEL),
        ),
    ]
