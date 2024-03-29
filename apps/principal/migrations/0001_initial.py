# Generated by Django 3.1.2 on 2021-01-03 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administracion', '0005_auto_20210102_0128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Imagenes')),
                ('title', models.CharField(max_length=80, verbose_name='Nombre')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.producto')),
            ],
            options={
                'verbose_name': 'Publicación',
                'verbose_name_plural': 'Publicaciones',
            },
        ),
    ]
