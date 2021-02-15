from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict

from apps.administracion.Views.Pedido.options import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name="Avatar", upload_to="avatar/%y/%m/", default='avatar\default\default_avatar.png',blank=True, null=True)
    salary = models.DecimalField(verbose_name="Sueldo", max_digits=30, decimal_places=2)
    rol = models.CharField(max_length=20)
    amount = models.DecimalField(verbose_name="Monto en posesión", max_digits=30, decimal_places=2)
    sueldo = models.DecimalField(verbose_name="Dinero de sueldo", max_digits=30, decimal_places=2)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def to_JSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

class Cliente(models.Model):
    name = models.CharField(verbose_name="Nombre y Apellido", max_length=40)
    description = models.CharField(verbose_name="Descripción", max_length=200, blank=True, null=True, default="")
    phone = models.CharField(verbose_name="Teléfono", max_length=15)
    adress = models.CharField(verbose_name="Dirección", max_length=60, blank=True, null=True)
    bought = models.SmallIntegerField(verbose_name="Compras", default=0, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name="Fecha de registro", auto_now_add=True)

    def __str__(self):
        return self.name

    def to_JSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class Material(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=40)
    price = models.DecimalField(verbose_name="Precio", max_digits=10, decimal_places=2)
    fusion_point = models.IntegerField(verbose_name="Punto de Fusión")

    def to_JSON(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"

class PlasticoDisponible(models.Model):
    color = models.CharField(verbose_name="Color", max_length=20)
    material = models.ForeignKey('Material', on_delete=models.PROTECT)
    available = models.PositiveIntegerField(verbose_name="Disponible", blank=True, null=True, default=1000)

    def __str__(self):
        return self.color + " - " + self.material.name + "- Gramos : " + str(self.available)
    
    class Meta:
        verbose_name = "Colores"
        verbose_name_plural = "Colores"

class Modelo(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=150)
    scale_x = models.DecimalField(verbose_name="Escala X", max_digits=10, decimal_places=2, default=100, blank=True, null=True)
    scale_y = models.DecimalField(verbose_name="Escala Y", max_digits=10, decimal_places=2, default=100, blank=True, null=True)
    scale_z = models.DecimalField(verbose_name="Escala Z", max_digits=10, decimal_places=2, default=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def to_JSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"

class Impresion(models.Model):
    hs = models.PositiveIntegerField(verbose_name="Horas")
    mins = models.PositiveIntegerField(verbose_name="Minutos")
    grs = models.PositiveIntegerField(verbose_name="Gramos")
    speed = models.DecimalField(verbose_name="Velocidad de Impresión", max_digits=7, decimal_places=2, default=35.00, blank=True, null=True)
    infill = models.PositiveSmallIntegerField(verbose_name="Relleno", default=10, blank=True, null=True)
    layer = models.DecimalField(verbose_name="Altura de Capa", max_digits=3, decimal_places=2, blank=True, null=True, default=0.2)
    nozzle = models.DecimalField(verbose_name="Boquilla", max_digits=2, decimal_places=1, blank=True, null=True, default=0.4)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    sub_total = models.DecimalField(verbose_name="Subtotal", max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        cadena = "Horas : " + str(self.hs) + "- Minutos : " + str(self.mins) + " - Gramos : " + str(self.grs)
        return cadena

    def to_JSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "Impresión"
        verbose_name_plural = "Impresiones"

class DetalleImpresion(models.Model):
    print = models.ForeignKey('Impresion', on_delete=models.CASCADE, blank=True, null=True)
    modelo = models.ForeignKey('Modelo', on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(verbose_name="Cantidad", default=1, blank=True, null=True)

    def to_JSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "Detalle Impresión"
        verbose_name_plural = "Detalle Impresiones"

class Producto(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=100)
    link = models.URLField(verbose_name="Link")
    price = models.DecimalField(verbose_name="Precio", max_digits=10, decimal_places=2, blank=True, null=True)
    date_created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)

    def __str__(self):
        return self.name

    def to_JSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class Datos(models.Model):
    date_created = models.DateTimeField(verbose_name="Fecha de Modificación", auto_now_add=True)
    hs_per_day = models.PositiveIntegerField(verbose_name="Horas de impresion diarias")
    print_days = models.PositiveIntegerField(verbose_name="Dias de impresion al mes")
    watts = models.PositiveIntegerField(verbose_name="Consumo de maquina")
    edelar = models.DecimalField(verbose_name="Tarifa Edelar", max_digits=10, decimal_places=2)
    fail_percentage = models.DecimalField(verbose_name="Porcentaje de Fallos", max_digits=10, decimal_places=2)
    hs_price = models.DecimalField(verbose_name="Precio hora de impresion", max_digits=10, decimal_places=2, blank=True, null=True)
    machines = models.PositiveIntegerField(verbose_name="Cantidad de Máquinas")

    def to_JSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "Datos cálculo de precios"
        verbose_name_plural = "Datos cálculo de precios"

class GastosMensuales(models.Model):
    date_created = models.DateTimeField(verbose_name="Fecha de Creacion", auto_now_add=True)
    name = models.CharField(verbose_name="Concepto", max_length=120)
    cost = models.DecimalField(verbose_name="Costo Unitario", max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(verbose_name="Cantidad")
    total = models.DecimalField(verbose_name="Total", max_digits=20, decimal_places=2, blank=True, null=True)
    description = models.CharField(verbose_name="Descripción", max_length=120, default="", blank=True, null=True)

    def to_JSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Gastos Mensuales"
        verbose_name_plural = "Gastos Mensuales"

class Caja(models.Model):
    amount = models.DecimalField(verbose_name="Monto Total", max_digits=30, decimal_places=2)
    amount_blaster = models.DecimalField(verbose_name="Monto emprendimiento", max_digits=30, decimal_places=2)
    amount_salaries = models.DecimalField(verbose_name="Monto sueldos", max_digits=30, decimal_places=2)
    date_created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)

    def to_JSON(self):
        item = model_to_dict(self)
        return item

class Extraccion(models.Model):
    amount = models.DecimalField(verbose_name="Monto de extraccion", max_digits=20, decimal_places=2)
    date = models.DateTimeField(verbose_name="Fecha de extraccion", auto_now_add=True)
    user_make = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    pay_user = models.ForeignKey('Profile', on_delete=models.SET_NULL, verbose_name="Pagado por", null=True)

    class Meta:
        verbose_name = "Extraccion"
        verbose_name_plural = "Extracciones"
    
    def to_JSON(self):
        item = model_to_dict(self)
        return item

class RegistroCaja(models.Model):
    date_created = models.DateTimeField(verbose_name="Fecha de creacion", auto_now_add=True)
    ingreso = models.DecimalField(verbose_name="Ingreso", max_digits=30, decimal_places=2, default=0, blank=True, null=True)
    egreso = models.DecimalField(verbose_name="Egreso", max_digits=30, decimal_places=2, default=0, blank=True, null=True)
    pay_by = models.ForeignKey('Profile', on_delete=models.SET_NULL, verbose_name="Pagado por", null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    concepto = models.CharField(verbose_name="Concepto", max_length=150)

    def to_JSON(self):
        item = model_to_dict(self)
        return item

class Pedido(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    date_created = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    total = models.DecimalField(verbose_name="Total", max_digits=30, decimal_places=2, blank=True, null=True)
    status = models.CharField(verbose_name="Estado", max_length=20, default="Recibido", blank=True, null=True)

    def to_JSON(self):
        item = model_to_dict(self)
        return item
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-id']

class DetallePedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveSmallIntegerField(verbose_name="Cantidad", default=1, blank=True, null=True)
    sub_total = models.DecimalField(verbose_name="Monto", max_digits=30, decimal_places=2, blank=True, null=True)
    status = models.CharField(verbose_name="Estado", max_length=25, default="No completo", blank=True, null=True)

    def to_JSON(self):
        item = model_to_dict(self)
        return item

class ImpresionPedido(models.Model):
    print = models.ForeignKey('Impresion', on_delete=models.CASCADE)
    pedido = models.ForeignKey('DetallePedido', on_delete=models.CASCADE)
    color = models.ForeignKey('PlasticoDisponible', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(verbose_name="Estado", max_length=20, default="No impreso", blank=True, null=True)

    def to_JSON(self):
        item = model_to_dict(self)
        return item

class CostoExtra(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    concept = models.CharField(verbose_name="Concepto", max_length=150)
    amount = models.DecimalField(verbose_name="Monto", max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = "Costo Extra"
        verbose_name_plural = "Costos Extra"
