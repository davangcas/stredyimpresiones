# Generated by Django 3.1.2 on 2021-01-21 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0007_costoextra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedido',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.producto'),
        ),
    ]
