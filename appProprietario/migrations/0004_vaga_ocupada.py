# Generated by Django 2.1.3 on 2019-10-12 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0003_remove_vaga_cliente_vaga'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaga',
            name='ocupada',
            field=models.BooleanField(default=False),
        ),
    ]
