# Generated by Django 2.1.3 on 2019-10-18 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0007_cliente_usuario_cli'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='is_cliente',
            field=models.BooleanField(default=True),
        ),
    ]