# Generated by Django 2.1.3 on 2019-10-19 21:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0010_remove_proprietario_nome_loc_prop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='usuario_cli',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='Cliente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='proprietario',
            name='usuario_prop',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='prop', to=settings.AUTH_USER_MODEL),
        ),
    ]
