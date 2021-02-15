from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.administracion.models import Modelo, Impresion, DetalleImpresion, Producto
from apps.administracion.Views.Modelos.forms import *

class ModeloCreate(CreateView):
    model = Modelo
    template_name = 'administracion/specific/Modelo/modelo_new.html'
    form_class = ModeloForm
    second_form_class = ModeloImpresionForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        impresion = self.kwargs['pk']
        return reverse_lazy('administracion:modelos', kwargs={'pk':impresion})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            modelo = form.save()
            detalle = form2.save(commit=False)
            detalle.print = Impresion.objects.get(pk=self.kwargs['pk'])
            detalle.modelo = Modelo.objects.get(pk=modelo.id)
            detalle.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(ModeloCreate, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        context['title'] = 'Nuevo Modelo'
        context['action_button'] = 'Agregar Modelo'
        return context

class ModeloList(ListView):
    model = DetalleImpresion
    template_name = 'administracion/specific/Modelo/modelo_list.html'

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
            'Acciones',
        ]
        context['add_button_name'] = 'Agregar Modelo'
        context['object_list'] = DetalleImpresion.objects.filter(print=self.kwargs['pk'])
        context['id_impresion'] = self.kwargs['pk']
        context['url_to_redirect'] = reverse_lazy('administracion:impresiones', kwargs={'pk':Producto.objects.get(pk=imp.producto.id).id})
        return context

class ModeloDelete(DeleteView):
    model = DetalleImpresion
    template_name = 'administracion/specific/Modelo/modelo_delete.html'
    success_url = reverse_lazy('administracion:productos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        impresion = DetalleImpresion.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('administracion:modelos', kwargs={'pk':impresion.print.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        modelo = Modelo.objects.get(pk=self.object.modelo.id)
        success_url = self.get_success_url()
        self.object.delete()
        modelo.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar modelo'
        return context

class ModeloUpdate(UpdateView):
    model = Modelo
    template_name = 'administracion/specific/Modelo/modelo_new.html'
    form_class = ModeloForm
    second_form_class = ModeloImpresionForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        impresion = DetalleImpresion.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('administracion:modelos', kwargs={'pk':impresion.print.id})
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            detalle = DetalleImpresion.objects.get(pk=self.kwargs['pk'])
            if form2.instance.quantity != None:
                detalle.quantity = form2.instance.quantity
                print(detalle.quantity)
            modelo = Modelo.objects.get(pk=detalle.modelo.id)
            modelo.name = form.instance.name
            modelo.scale_x = form.instance.scale_x
            modelo.scale_y = form.instance.scale_y
            modelo.scale_z = form.instance.scale_z
            modelo.save()
            detalle.save()
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
        context['title'] = 'Editar Modelo'
        context['action_button'] = 'Modificar Modelo'
        return context
