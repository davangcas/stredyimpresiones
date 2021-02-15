# Generated by Django 3.1.2 on 2021-02-15 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0009_impresion_nozzle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impresionpedido',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administracion.plasticodisponible'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/default/default_avatar.png', null=True, upload_to='avatar/%y/%m/', verbose_name='Avatar'),
        ),
    ]
