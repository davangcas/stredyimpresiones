# Generated by Django 3.1.2 on 2021-01-02 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0004_auto_20210102_0127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'ordering': ['-id'], 'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
    ]
