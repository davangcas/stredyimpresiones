import decimal

from apps.administracion.models import Datos, GastosMensuales, Profile, Impresion, Producto, Pedido, DetallePedido, ImpresionPedido, CostoExtra

def precio(edelar, dias, consumo, horas, sueldos, gastos, maquinas, fallo):
    dato = dias * horas
    consumo_total = consumo / 1000
    luz = consumo_total * dato
    luz_total = luz * float(edelar) * float(maquinas)
    precio = float(sueldos) + float(gastos) + luz_total
    precio_dividido = precio / dato
    machines = precio_dividido / maquinas
    fail = 1 + (fallo / 100)
    total = machines * float(fail)
    return total

def precio_producto(hs, minutos, gramos, material, precio_hora):
    horas_totales = float(hs) + (float(minutos) / 60)
    precio_hs_impresion = float(horas_totales) * float(precio_hora)
    precio_grs = float(gramos) * (float(material) / 1000 )
    precio = precio_grs + precio_hs_impresion
    precio_final = (10 - (precio % 10))
    precio_final = precio_final + precio
    return precio_final

def actualizar_precios():
    dato = Datos.objects.last()
    impresiones = Impresion.objects.all()
    productos = Producto.objects.all()
    for imp in impresiones:
        imp.sub_total = precio_producto(imp.hs, imp.mins, imp.grs, imp.material.price, dato.hs_price)
        imp.save()
    for pro in productos:
        prints = Impresion.objects.filter(producto=pro.pk)
        producto_price = 0
        for print in prints:
            producto_price = producto_price + print.sub_total
        costos = CostoExtra.objects.filter(product=pro)
        precio_costos = 0
        for costo in costos:
            precio_costos = precio_costos + costo.amount
        pro.price = producto_price + precio_costos
        pro.save()

def actualizar_datos():
    datos = Datos.objects.last()
    gastos = GastosMensuales.objects.all()
    sueldos = Profile.objects.all()
    sueldos_total = 0
    gastos_totales = 0
    for g in gastos:
        gastos_totales = gastos_totales + g.total
    for s in sueldos:
        sueldos_total = sueldos_total + s.salary
    datos.hs_price = precio(datos.edelar, datos.print_days, datos.watts, datos.hs_per_day, sueldos_total, gastos_totales, datos.machines, datos.fail_percentage)
    datos.save()

def precio_gramos(id_pedido):
    detalles = DetallePedido.objects.filter(pedido=id_pedido)
    precio_total = 0
    for detalle in detalles:
        impresiones_detalles = ImpresionPedido.objects.filter(pedido=detalle.id)
        for impresion in impresiones_detalles:
            gramos = impresion.print.grs
            material_precio = impresion.color.material.price
            precio_gramos_impresion = float(gramos) * (float(material_precio) / 1000)
            precio_total = precio_total + precio_gramos_impresion
    return precio_total

def precio_costos(id_pedido):
    detalles = DetallePedido.objects.filter(pedido=id_pedido)
    precio_total = 0
    for detalle in detalles:
        precio_medio = 0
        costos_extra = CostoExtra.objects.filter(product=detalle.producto)
        for costo in costos_extra:
            precio_medio = precio_medio + costo.amount
        precio_medio = float(precio_medio) * float(detalle.cantidad)
        precio_total = precio_total + precio_medio
    return precio_total
