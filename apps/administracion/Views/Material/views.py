from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.views import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.administracion.functions import precio_producto, actualizar_precios
from apps.administracion.models import Material, PlasticoDisponible, Datos, Impresion, Producto
from apps.administracion.Views.Material.forms import MaterialForm, ColorForm

def nuevo_rollo(request, id):
    color = PlasticoDisponible.objects.get(pk=id)
    color.available = color.available + 1000
    color.save()
    success_url = reverse_lazy('administracion:colores')
    return HttpResponseRedirect(success_url)

class MaterialListView(ListView):
    model = Material
    template_name = 'administracion/specific/Material/material_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Materiales'
        context['title_table'] = 'Lista de Materiales'
        context['table_id'] = 'Materiales'
        context['table_fields'] = [
            'Nombre',
            'Precio / Kg',
            'Punto de Fusión',
            'Acciones',
        ]
        context['add_button_name'] = 'Nuevo Material'
        return context

class MaterialCreateView(CreateView):
    model = Material
    template_name = 'administracion/specific/Material/material_new.html'
    form_class = MaterialForm
    success_url = reverse_lazy('administracion:materiales')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Material'
        context['action_button'] = 'Agregar Nuevo Material'
        return context

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'administracion/specific/Material/material_new.html'
    success_url = reverse_lazy('administracion:materiales')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        self.object = form.save()
        actualizar_precios()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificar Gasto'
        context['action_button'] = 'Guardar Cambios'
        return context

class ColorListView(ListView):
    model = PlasticoDisponible
    template_name = 'administracion/specific/Material/color_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Colores Disponibles'
        context['title_table'] = 'Lista de Colores Disponibles'
        context['table_id'] = 'Colores'
        context['table_fields'] = [
            'ID',
            'Material',
            'Color',
            'Gramos Disponibles',
            'Acciones',
        ]
        context['add_button_name'] = 'Nuevo Color'
        return context

class ColorCreateView(CreateView):
    model = PlasticoDisponible
    template_name = 'administracion/specific/Material/color_new.html'
    form_class = ColorForm
    success_url = reverse_lazy('administracion:colores')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar Color'
        context['action_button'] = 'Agregar Nuevo Color'
        return context

class ColorUpdate(UpdateView):
    model = PlasticoDisponible
    template_name = 'administracion/specific/Material/color_new.html'
    form_class = ColorForm
    success_url = reverse_lazy('administracion:colores')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Color'
        context['action_button'] = 'Guardar Cambios'
        return context

class ColorDelete(DeleteView):
    model = PlasticoDisponible
    template_name = "administracion/specific/Material/color_delete.html"
    success_url = reverse_lazy('administracion:colores')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Color'
        return context

