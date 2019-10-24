# Generated by Django 2.1.3 on 2019-10-22 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0011_auto_20191019_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente_vaga',
            name='cliente',
            field=models.OneToOneField(default='', editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]