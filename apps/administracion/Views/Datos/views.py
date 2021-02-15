from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.administracion.Views.Datos.forms import DatosForm
from apps.administracion.functions import *
from apps.administracion.models import Datos, GastosMensuales, Profile, Impresion, Producto

class DatosListView(ListView):
    model = Datos
    template_name = 'administracion/specific/Datos/datos_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Datos'
        context['title_table'] = 'Historial de Datos utilizados'
        context['table_id'] = 'Datos'
        context['table_fields'] = [
            'ID',
            'Fecha de modificación',
            'Horas de impresión diarias',
            'Dias imprimiendo',
            'Consumo (Watts)',
            'Tarifa Edelar',
            'Porcentaje de Fallos',
            'Maquinas',
            'Precio Hora de Impresion',
        ]
        context['add_button_name'] = 'Modificar Datos'
        context['dat'] = Datos.objects.last()
        return context

class DatosCreateView(CreateView):
    model = Datos
    template_name = 'administracion/specific/Datos/datos_edit.html'
    form_class = DatosForm
    success_url = reverse_lazy('administracion:datos_detail')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            gastos = GastosMensuales.objects.all()
            sueldos = Profile.objects.all()
            sueldos_total = 0
            gastos_totales = 0
            for g in gastos:
                gastos_totales = gastos_totales + g.total
            for s in sueldos:
                sueldos_total = sueldos_total + s.salary
            formulario = form.save(commit=False)
            formulario.hs_price = precio(formulario.edelar, formulario.print_days, formulario.watts, formulario.hs_per_day, sueldos_total, gastos_totales, formulario.machines, formulario.fail_percentage)
            formulario.save()
            actualizar_precios()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevos Datos'
        context['action_button'] = 'Modificar Datos'
        return context
