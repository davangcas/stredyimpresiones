from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.administracion.models import Impresion, Datos, Producto, CostoExtra
from apps.administracion.Views.Impresion.forms import ImpresionForm
from apps.administracion.functions import *

class ImpresionCreate(CreateView):
    model = Impresion
    form_class = ImpresionForm
    template_name = 'administracion/specific/Impresion/impresion_new.html'
    success_url = reverse_lazy('administracion:productos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        producto = Producto.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('administracion:impresiones', kwargs={'pk':producto.id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            impresion = form.save(commit=False)
            impresion.producto_id = self.kwargs['pk']
            dato = Datos.objects.last()
            impresion.sub_total = precio_producto(impresion.hs, impresion.mins, impresion.grs, impresion.material.price, dato.hs_price)
            impresion.save()
            impresiones = Impresion.objects.filter(producto=self.kwargs['pk'])
            producto = Producto.objects.get(pk=self.kwargs['pk'])
            monto = 0
            for imp in impresiones:
                monto = monto + imp.sub_total
            producto.price = monto
            producto.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nueva Impresion'
        context['action_button'] = 'Añadir Impresión'
        return context

class ImpresionList(ListView):
    model = Impresion
    template_name = 'administracion/specific/Impresion/impresion_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Producto.objects.get(pk=self.kwargs['pk']).name
        context['title_table'] = 'Impresiones del producto'
        context['table_id'] = 'Impresiones'
        context['table_fields'] = [
            'Horas',
            'Minutos',
            'Gramos',
            'Material',
            'Boquilla',
            'Relleno',
            'Velocidad',
            'Altura de capa',
            'Acciones',
        ]
        context['add_button_name'] = 'Agregar Impresión'
        context['object_list'] = Impresion.objects.filter(producto=self.kwargs['pk'])
        context['id_producto'] = self.kwargs['pk']
        context['producto'] = Producto.objects.get(pk=self.kwargs['pk'])
        context['costos'] = CostoExtra.objects.filter(product=self.kwargs['pk'])
        return context

class ImpresionUpdate(UpdateView):
    model = Impresion
    form_class = ImpresionForm
    template_name = 'administracion/specific/Impresion/impresion_new.html'
    success_url = reverse_lazy('administracion:productos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        impresion = Impresion.objects.get(pk=self.kwargs['pk'])
        producto = Producto.objects.get(pk=impresion.producto.id)
        return reverse_lazy('administracion:impresiones', kwargs={'pk':producto.id})

    def form_valid(self, form):
        dato = Datos.objects.last()
        form.instance.sub_total = precio_producto(form.instance.hs, form.instance.mins, form.instance.grs, form.instance.material.price, dato.hs_price)
        self.object = form.save()
        impresiones = Impresion.objects.filter(producto=form.instance.producto.id)
        producto = Producto.objects.get(pk=form.instance.producto.id)
        monto = 0
        for imp in impresiones:
            monto = monto + imp.sub_total
        costos = CostoExtra.objects.filter(product=producto)
        precio_costos = 0
        for costo in costos:
            precio_costos = precio_costos + costo.amount
        producto.price = monto + precio_costos
        producto.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Impresion'
        context['action_button'] = 'Guardar Cambios'
        return context

class ImpresionDelete(DeleteView):
    model = Impresion
    template_name = 'administracion/specific/Impresion/impresion_delete.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        impresion = Impresion.objects.get(pk=self.kwargs['pk'])
        return reverse_lazy('administracion:impresiones', kwargs={'pk':impresion.producto.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        producto = Producto.objects.get(pk=self.object.producto.id)
        self.object.delete()
        dato = Datos.objects.last()
        impresiones = Impresion.objects.filter(producto=producto.id)
        monto = 0
        for imp in impresiones:
            monto = monto + imp.sub_total
        producto.price = monto
        producto.save()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar impresion'
        return context
