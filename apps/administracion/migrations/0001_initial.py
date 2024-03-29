# Generated by Django 3.1.2 on 2020-10-11 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Monto Total')),
                ('amount_blaster', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Monto emprendimiento')),
                ('amount_salaries', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Monto sueldos')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Nombre y Apellido')),
                ('description', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Descripción')),
                ('phone', models.CharField(max_length=15, verbose_name='Teléfono')),
                ('adress', models.CharField(blank=True, max_length=60, null=True, verbose_name='Dirección')),
                ('bought', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Compras')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Modificación')),
                ('hs_per_day', models.PositiveIntegerField(verbose_name='Horas de impresion diarias')),
                ('print_days', models.PositiveIntegerField(verbose_name='Dias de impresion al mes')),
                ('watts', models.PositiveIntegerField(verbose_name='Consumo de maquina')),
                ('edelar', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tarifa Edelar')),
                ('fail_percentage', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Porcentaje de Fallos')),
                ('hs_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio hora de impresion')),
                ('machines', models.PositiveIntegerField(verbose_name='Cantidad de Máquinas')),
            ],
            options={
                'verbose_name': 'Datos cálculo de precios',
                'verbose_name_plural': 'Datos cálculo de precios',
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Cantidad')),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True, verbose_name='Monto')),
                ('status', models.CharField(blank=True, default='No completo', max_length=25, null=True, verbose_name='Estado')),
            ],
        ),
        migrations.CreateModel(
            name='GastosMensuales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('name', models.CharField(max_length=120, verbose_name='Concepto')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Costo Unitario')),
                ('quantity', models.PositiveSmallIntegerField(verbose_name='Cantidad')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Total')),
                ('description', models.CharField(blank=True, default='', max_length=120, null=True, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Gastos Mensuales',
                'verbose_name_plural': 'Gastos Mensuales',
            },
        ),
        migrations.CreateModel(
            name='Impresion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hs', models.PositiveIntegerField(verbose_name='Horas')),
                ('mins', models.PositiveIntegerField(verbose_name='Minutos')),
                ('grs', models.PositiveIntegerField(verbose_name='Gramos')),
                ('speed', models.DecimalField(blank=True, decimal_places=2, default=35.0, max_digits=7, null=True, verbose_name='Velocidad de Impresión')),
                ('infill', models.PositiveSmallIntegerField(blank=True, default=10, null=True, verbose_name='Relleno')),
                ('layer', models.DecimalField(blank=True, decimal_places=2, default=0.2, max_digits=3, null=True, verbose_name='Altura de Capa')),
                ('sub_total', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Subtotal')),
            ],
            options={
                'verbose_name': 'Impresión',
                'verbose_name_plural': 'Impresiones',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='Nombre')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('fusion_point', models.IntegerField(verbose_name='Punto de Fusión')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materiales',
            },
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Nombre')),
                ('scale_x', models.DecimalField(blank=True, decimal_places=2, default=100, max_digits=10, null=True, verbose_name='Escala X')),
                ('scale_y', models.DecimalField(blank=True, decimal_places=2, default=100, max_digits=10, null=True, verbose_name='Escala Y')),
                ('scale_z', models.DecimalField(blank=True, decimal_places=2, default=100, max_digits=10, null=True, verbose_name='Escala Z')),
            ],
            options={
                'verbose_name': 'Modelo',
                'verbose_name_plural': 'Modelos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Nombre')),
                ('link', models.URLField(verbose_name='Link')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='avatar\\default\\default_avatar.png', null=True, upload_to='avatar/%y/%m/', verbose_name='Avatar')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Sueldo')),
                ('rol', models.CharField(max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Monto en posesión')),
                ('sueldo', models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Dinero de sueldo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Perfil',
                'verbose_name_plural': 'Perfiles',
            },
        ),
        migrations.CreateModel(
            name='RegistroCaja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('ingreso', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=30, null=True, verbose_name='Ingreso')),
                ('egreso', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=30, null=True, verbose_name='Egreso')),
                ('concepto', models.CharField(max_length=150, verbose_name='Concepto')),
                ('pay_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.profile', verbose_name='Pagado por')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlasticoDisponible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=20, verbose_name='Color')),
                ('available', models.PositiveIntegerField(blank=True, default=1000, null=True, verbose_name='Disponible')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.material')),
            ],
            options={
                'verbose_name': 'Colores',
                'verbose_name_plural': 'Colores',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True, verbose_name='Total')),
                ('status', models.CharField(blank=True, default='Recibido', max_length=20, null=True, verbose_name='Estado')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.cliente')),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
            },
        ),
        migrations.CreateModel(
            name='ImpresionPedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, default='No impreso', max_length=20, null=True, verbose_name='Estado')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.plasticodisponible')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.detallepedido')),
                ('print', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.impresion')),
            ],
        ),
        migrations.AddField(
            model_name='impresion',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.material'),
        ),
        migrations.AddField(
            model_name='impresion',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.producto'),
        ),
        migrations.CreateModel(
            name='Extraccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Monto de extraccion')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de extraccion')),
                ('pay_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.profile', verbose_name='Pagado por')),
                ('user_make', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Extraccion',
                'verbose_name_plural': 'Extracciones',
            },
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracion.pedido'),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='administracion.producto'),
        ),
        migrations.CreateModel(
            name='DetalleImpresion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Cantidad')),
                ('modelo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.modelo')),
                ('print', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administracion.impresion')),
            ],
            options={
                'verbose_name': 'Detalle Impresión',
                'verbose_name_plural': 'Detalle Impresiones',
            },
        ),
    ]
