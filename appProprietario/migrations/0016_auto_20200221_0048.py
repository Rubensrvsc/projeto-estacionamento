# Generated by Django 3.0.2 on 2020-02-21 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appProprietario', '0015_auto_20200221_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente_vaga',
            name='hora_saida',
            field=models.DateTimeField(null=True),
        ),
    ]