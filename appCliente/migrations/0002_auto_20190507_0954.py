# Generated by Django 2.1.3 on 2019-05-07 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appCliente', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='senha',
            new_name='senha_cliente',
        ),
    ]
