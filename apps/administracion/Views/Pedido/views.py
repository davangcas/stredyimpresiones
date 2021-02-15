from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from apps.administracion.models import *
from apps.administracion.Views.Pedido.forms import *
from apps.administracion.functions import precio_gramos, precio_costos

def impresion_cambio(request, id):
    impresion_pedido = ImpresionPedido.objects.get(pk=id)
    if impresion_pedido.status == 'No impreso':
        impresion_pedido.status = "Imprimiendose"
        color = PlasticoDisponible.objects.get(pk=impresion_pedido.color.id)
        color.available = color.available - impresion_pedido.print.grs
        color.save()
        impresion_pedido.save()
    elif impresion_pedido.status == 'Imprimiendose':
        impresion_pedido.status = 'Listo'
        impresion_pedido.save()
        impresiones = ImpresionPedido.objects.filter(pedido=impresion_pedido.pedido.id)
        cantidad = impresiones.count()
        acumulador = 0
        for imp in impresiones:
            if imp.status == 'Listo':
                acumulador = acumulador + 1
        if acumulador == cantidad:
            detalle = DetallePedido.objects.get(pk=impresion_pedido.pedido.id)
            detalle.status = 'Listo'
            detalle.save()
            detalles = DetallePedido.objects.filter(pedido=detalle.pedido.id)
            cantidad = detalles.count()
            acumulador = 0
            for det in detalles:
                if det.status == 'Listo':
                    acumulador = acumulador + 1
            if acumulador == cantidad:
                pedido = Pedido.objects.get(pk=detalle.pedido.id)
                pedido.status = 'Listo'
                pedido.save()
    success_url = reverse_lazy('administracion:pedidos_impresiones_realizar')
    return HttpResponseRedirect(success_url)

def impresion_cancelar(request, id):
    impresion_pedido = ImpresionPedido.objects.get(pk=id)
    impresion_pedido.status = "No impreso"
    impresion_pedido.save()
    success_url = reverse_lazy('administracion:pedidos_impresiones_realizar')
    return HttpResponseRedirect(success_url)

def pedido_pagado(request, id):
    pedido = Pedido.objects.get(pk=id)
    pedido.status = 'Pagado'
    pedido.cliente.bought = pedido.cliente.bought + 1
    pedido.save()
    gramos_precio = precio_gramos(pedido.id)
    costos = precio_costos(pedido.id)
    perfil = Profile.objects.get(user=request.user)
    perfil.amount = perfil.amount + pedido.total
    perfil.save()
    caja_ultima = Caja.objects.last()
    gastos = GastosMensuales.objects.all()
    perfiles = Profile.objects.all()
    gastos_totales = 0
    sueldos = 0
    for g in gastos:
        gastos_totales = gastos_totales + g.total
    for p in perfiles:
        sueldos = sueldos + p.salary
    porcentaje_blaster = (gastos_totales) / (gastos_totales + sueldos)
    porcentaje_sueldos = (sueldos) / (gastos_totales + sueldos)
    reparticion = float(pedido.total) - gramos_precio - costos
    caja_ultima.amount = caja_ultima.amount + pedido.total
    caja_ultima.amount_blaster = float(caja_ultima.amount_blaster) + (float(reparticion) * float(porcentaje_blaster)) + float(gramos_precio) + float(costos)
    caja_ultima.amount_salaries = float(caja_ultima.amount_salaries) + (float(reparticion) * float(porcentaje_sueldos))
    caja_ultima.save()
    for p in perfiles:
        porcentaje_sueldo = p.salary / sueldos
        ultimo_pedido = float(reparticion) * float(porcentaje_sueldos)
        p.sueldo = float(p.sueldo) + (float(ultimo_pedido) * float(porcentaje_sueldo))
        p.save()
    success_url = reverse_lazy('administracion:pedidos')
    return HttpResponseRedirect(success_url)

def pedido_cancelado(request, id):
    pedido = Pedido.objects.get(pk=id)
    pedido.status = 'Cancelado'
    pedido.save()
    success_url = reverse_lazy('administracion:pedidos')
    return HttpResponseRedirect(success_url)

class PedidoList(ListView):
    model = Pedido
    template_name = 'administracion/specific/Pedido/pedidos_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        pedidos = Pedido.objects.all().order_by('-id')
        return pedidos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pedidos'
        context['title_table'] = 'Lista de pedidos'
        context['table_id'] = 'Pedidos'
        context['table_fields'] = [
            'ID',
            'Fecha de entrada',
            'Cliente',
            'Monto',
            'Estado',
            'Acciones',
        ]
        context['add_button_name'] = 'Nuevo Pedido'
        return context

class PedidoCreate(CreateView):
    model = DetallePedido
    form_class = DetallePedidoForm
    second_form_class = PedidoForm
    template_name = 'administracion/specific/Pedido/pedido_new.html'
    success_url = reverse_lazy('administracion:pedidos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            detalle = form.save(commit=False)
            detalle.pedido = form2.save(commit=False)
            detalle.sub_total = detalle.producto.price * detalle.cantidad
            detalle.pedido.total = detalle.sub_total
            detalle.pedido.save()
            detalle.save()
            impresiones = Impresion.objects.filter(producto=detalle.producto.id)
            for i in range(detalle.cantidad):
                for imp in impresiones:
                    impresion_pedido = ImpresionPedido(print=imp, pedido=detalle)
                    impresion_pedido.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        context['title'] = 'Nuevo Pedido'
        context['action_button'] = 'Crear Pedido'
        return context

class PedidoDetalleList(ListView):
    model = DetallePedido
    template_name = 'administracion/specific/Pedido/pedido_detalle_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del pedido'
        context['title_table'] = 'Lista de productos'
        context['table_id'] = 'Pedidos'
        context['table_fields'] = [
            'Producto',
            'Cantidad',
            'Sub total',
            'Estado',
            'Acciones',
        ]
        context['add_button_name'] = 'Agregar producto al pedido'
        context['object_list'] = DetallePedido.objects.filter(pedido=self.kwargs['pk'])
        context['id_pedido'] = self.kwargs['pk']
        context['pedido_estado'] = Pedido.objects.get(pk=self.kwargs['pk'])
        return context

class PedidoClienteCreate(CreateView):
    model = DetallePedido
    form_class = DetallePedidoForm
    template_name = 'administracion/specific/Pedido/pedido_cliente_new.html'
    success_url = reverse_lazy('administracion:pedidos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            detalle = form.save(commit=False)
            pedido = Pedido(cliente=Cliente.objects.get(pk=self.kwargs['pk']))
            detalle.sub_total = detalle.producto.price * detalle.cantidad
            pedido.total = detalle.sub_total
            detalle.pedido = pedido
            pedido.save()
            detalle.save()
            impresiones = Impresion.objects.filter(producto=detalle.producto.id)
            for i in range(detalle.cantidad):
                for imp in impresiones:
                    impresion_pedido = ImpresionPedido(print=imp, pedido=detalle)
                    impresion_pedido.save()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Pedido'
        context['action_button'] = 'Crear pedido'
        return context

class ImpresionesRealizarList(ListView):
    model = ImpresionPedido
    template_name = 'administracion/specific/Pedido/impresiones_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pedido de ' + DetallePedido.objects.get(pk=self.kwargs['pk']).pedido.cliente.name
        context['title_table'] = 'Lista de impresiones a realizar'
        context['table_id'] = 'Impresiones'
        context['table_fields'] = [
            'Id',
            'Cliente',
            'Producto',
            'Color',
            'Estado',
            'Acciones',
        ]
        context['object_list'] = ImpresionPedido.objects.filter(pedido=self.kwargs['pk'])
        context['id_pedido'] = self.kwargs['pk']
        return context

class ImpresionDetalleUpdate(UpdateView):
    model = ImpresionPedido
    form_class = ImpresionForm
    template_name = 'administracion/specific/Pedido/impresion_edit.html'
    success_url = reverse_lazy('administracion:pedidos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        impresion = ImpresionPedido.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('administracion:impresiones_detalle', kwargs={'pk':impresion.pedido.id})

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Impresion'
        context['action_button'] = 'Guardar Cambios'
        return context

class ImpresionDetalleVer(ListView):
    model = DetalleImpresion
    template_name = 'administracion/specific/Pedido/impresion_datos.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        imp = Impresion.objects.get(pk=self.kwargs['pk'])
        context['title'] = Producto.objects.get(pk=imp.producto.id).name
        context['title_table'] = 'Modelos de la Impresion'
        context['table_id'] = 'Modelos'
        context['table_fields'] = [
            'Nombre',
            'Escala X',
            'Escala Y',
            'Escala Z',
            'Veces en la impresion',
        ]
        context['add_button_name'] = 'Agregar Modelo'
        context['object_list'] = DetalleImpresion.objects.filter(print=self.kwargs['pk'])
        context['impresion'] = Impresion.objects.get(pk=self.kwargs['pk'])
        context['id_impresion'] = self.kwargs['pk']
        context['url_to_redirect'] = reverse_lazy('administracion:impresiones', kwargs={'pk':Producto.objects.get(pk=imp.producto.id).id})
        return context

class ImpresionPedidoTodas(ListView):
    model = ImpresionPedido
    template_name = 'administracion/specific/Pedido/impresiones_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Impresiones a realizar'
        context['title_table'] = 'Lista de todas las impresiones a realizar'
        context['table_id'] = 'Impresiones'
        context['table_fields'] = [
            'Id',
            'Cliente',
            'Producto',
            'Color',
            'Estado',
            'Acciones',
        ]
        context['object_list'] = ImpresionPedido.objects.exclude(status='Listo').exclude(pedido__pedido__status='Cancelado')
        return context

class PedidoProductoAgregar(CreateView):
    model = DetallePedido
    form_class = DetallePedidoForm
    template_name = 'administracion/specific/Pedido/pedido_cliente_new.html'
    success_url = reverse_lazy('administracion:pedidos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            detalle = form.save(commit=False)
            pedido = Pedido.objects.get(pk=self.kwargs['pk'])
            pedido.status = 'Recibido'
            detalle.sub_total = detalle.producto.price * detalle.cantidad
            pedido.total = pedido.total + detalle.sub_total
            detalle.pedido = pedido
            pedido.save()
            detalle.save()
            impresiones = Impresion.objects.filter(producto=detalle.producto.id)
            for i in range(detalle.cantidad):
                for imp in impresiones:
                    impresion_pedido = ImpresionPedido(print=imp, pedido=detalle)
                    impresion_pedido.save()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar producto al pedido'
        context['action_button'] = 'Agregar'
        return context
