# Generated by Django 3.1.2 on 2021-01-03 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_auto_20210103_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='image',
            field=models.ImageField(upload_to='publicacion/%y/%m', verbose_name='Imagen'),
        ),
    ]
