# Generated by Django 2.1.3 on 2019-10-08 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appProprietario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cli', models.CharField(max_length=255)),
                ('email_cli', models.EmailField(max_length=254)),
                ('usuario_cli', models.OneToOneField(default='', editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Cliente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='vaga',
            name='prop',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='appProprietario.Proprietario'),
        ),
        migrations.AddField(
            model_name='vaga',
            name='cliente_vaga',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='appProprietario.Cliente'),
        ),
    ]
