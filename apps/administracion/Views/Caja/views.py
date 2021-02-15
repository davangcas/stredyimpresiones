from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_delete

from apps.administracion.Views.Caja.forms import *
from apps.administracion.models import GastosMensuales, Datos, Profile, Impresion, Producto, Extraccion, Caja, RegistroCaja
from apps.administracion.functions import *

class GastosListView(ListView):
    model = GastosMensuales
    template_name = 'administracion/specific/Caja/caja_gastos.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Costos Mensuales'
        context['title_table'] = 'Costos Mensuales'
        context['table_id'] = 'Gastos'
        context['table_fields'] = [
            'Concepto',
            'Monto',
            'Descripción',
            'Acciones',
        ]
        context['add_button_name'] = 'Nuevo Costo'
        return context

class GastosCreateView(CreateView):
    model = GastosMensuales
    form_class = GastosForm
    template_name = 'administracion/specific/Caja/caja_gastos_new.html'
    success_url = reverse_lazy('administracion:gastos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.total = formulario.cost * formulario.quantity
            formulario.save()
            actualizar_datos()
            actualizar_precios()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Costo'
        context['action_button'] = 'Agregar Nuevo Costo'
        return context

class GastosDeleteView(DeleteView):
    model = GastosMensuales
    template_name = 'administracion/specific/Caja/caja_gastos_delete.html'
    success_url = reverse_lazy('administracion:gastos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        actualizar_datos()
        actualizar_precios()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar costo mensual'
        return context

class GastosUpdateView(UpdateView):
    model = GastosMensuales
    form_class = GastosForm
    template_name = 'administracion/specific/Caja/caja_gastos_new.html'
    success_url = reverse_lazy('administracion:gastos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    #def post(self, request, *args, **kwargs):
    #    request.POST = request.POST.copy()
    #    request.POST['total'] = float(request.POST['cost']) * int(request.POST['quantity'])
    #   return super(GastosUpdateView, self).post(request, **kwargs)

    def form_valid(self, form):
        form.instance.total = form.instance.cost * form.instance.quantity
        self.object = form.save()
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
        actualizar_precios()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificar Gasto'
        context['action_button'] = 'Guardar Cambios'
        return context

class ExtraccionCreate(CreateView):
    model = Extraccion
    template_name = 'administracion/specific/Caja/caja_extraccion.html'
    form_class = ExtraccionForm
    success_url = reverse_lazy('administracion:index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        saldo_disponible = Profile.objects.get(user=request.user.id).amount
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.user_make = request.user
            formulario.save()
            perfil = Profile.objects.get(user=request.user.id)
            perfil.sueldo = perfil.sueldo - formulario.amount
            perfil.save()
            perfil_pagador = Profile.objects.get(pk=formulario.pay_user.id)
            perfil_pagador.amount = perfil_pagador.amount - formulario.amount
            perfil_pagador.save()
            caja_ultima = Caja.objects.last()
            caja = Caja()
            caja.amount = caja_ultima.amount
            caja.amount_blaster = caja_ultima.amount_blaster
            caja.amount_salaries = caja_ultima.amount_salaries
            caja.amount = caja.amount - formulario.amount
            caja.amount_salaries = caja.amount_salaries - formulario.amount
            caja.save()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Extraccion'
        context['action_button'] = 'Realizar Extraccion'
        return context

class RegistroCreate(CreateView):
    model = RegistroCaja
    template_name = 'administracion/specific/Caja/caja_registro_new.html'
    form_class = RegistroForm
    success_url = reverse_lazy('administracion:caja_movimientos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            formulario = form.save(commit=False)
            formulario.user = request.user
            perfil = Profile.objects.get(user=request.user.id)
            perfil.amount = perfil.amount - formulario.egreso + formulario.ingreso
            perfil.save()
            caja_ultima = Caja.objects.last()
            caja = Caja()
            caja.amount = caja_ultima.amount
            caja.amount = caja.amount - formulario.egreso + formulario.ingreso
            caja.amount_blaster = caja_ultima.amount_blaster
            caja.amount_blaster = caja.amount_blaster + formulario.ingreso - formulario.egreso
            caja.amount_salaries = caja_ultima.amount_salaries
            caja.save()
            formulario.save()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro en caja'
        context['action_button'] = 'Nuevo registro'
        context['caja'] = Caja.objects.last()
        return context

class CajaList(ListView):
    model = RegistroCaja
    template_name = 'administracion/specific/Caja/caja_movimientos.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Movimientos de caja'
        context['title_table'] = 'Registro de movimientos'
        context['table_id'] = 'Registro'
        context['table_fields'] = [
            'ID',
            'Fecha',
            'Concepto',
            'Ingreso',
            'Egreso',
            'Pagado por',
            'Realizado por',
        ]
        context['add_button_name'] = 'Nuevo Movimiento'
        context['caja'] = Caja.objects.last()
        context['e_propia'] = Extraccion.objects.filter(user_make=self.request.user)
        context['e_todos'] = Extraccion.objects.exclude(user_make=self.request.user)
        return context
