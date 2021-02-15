from django.contrib import admin
from apps.administracion.models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'avatar',
        'salary',
    ]

class ClienteAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'bought',
        'date_created',
    ]

class DatosAdmin(admin.ModelAdmin):
    list_display = [
        'date_created',
        'hs_per_day',
        'print_days',
        'hs_price',
    ]

class GastosAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'cost',
        'total',
        'description',
        'date_created',
    ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Datos, DatosAdmin)
admin.site.register(GastosMensuales, GastosAdmin)
admin.site.register(Impresion)
admin.site.register(Producto)
admin.site.register(Modelo)
admin.site.register(DetalleImpresion)
admin.site.register(Extraccion)
admin.site.register(Caja)
admin.site.register(Pedido)
admin.site.register(RegistroCaja)
admin.site.register(PlasticoDisponible)
admin.site.register(ImpresionPedido)
admin.site.register(DetallePedido)
