# Generated by Django 2.1.3 on 2019-10-18 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appProprietario', '0006_auto_20191017_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='usuario_cli',
            field=models.OneToOneField(default='', editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cliente', to=settings.AUTH_USER_MODEL),
        ),
    ]
