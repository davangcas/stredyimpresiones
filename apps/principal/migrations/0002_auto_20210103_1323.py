# Generated by Django 3.1.2 on 2021-01-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='image',
            field=models.ImageField(upload_to='publicacion/%y/%m', verbose_name='Imagenes'),
        ),
    ]
