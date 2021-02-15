from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render

from apps.administracion.functions import precio_producto
from apps.administracion.models import Producto, Impresion, Datos, Modelo, DetalleImpresion
from apps.administracion.Views.Producto.forms import ProductoForm, ImpresionForm

class ProductoListView(ListView):
    model = Producto
    template_name = 'administracion/specific/Producto/producto_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Productos'
        context['title_table'] = 'Productos'
        context['table_id'] = 'Productos'
        context['table_fields'] = [
            'ID',
            'Nombre',
            'Link',
            'Precio',
            'Acciones',
        ]
        context['add_button_name'] = 'Nuevo Producto'
        return context

class ProductoCreateView(CreateView):
    model = Impresion
    template_name = 'administracion/specific/Producto/producto_new.html'
    form_class = ImpresionForm
    second_form_class = ProductoForm
    success_url = reverse_lazy('administracion:productos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        producto = Producto.objects.last()
        return reverse_lazy('administracion:impresiones', kwargs={'pk':producto.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            dato = Datos.objects.last()
            impresion = form.save(commit=False)
            impresion.producto = form2.save(commit=False)
            impresion.sub_total = precio_producto(impresion.hs, impresion.mins, impresion.grs, impresion.material.price, dato.hs_price)
            impresion.producto.price = impresion.sub_total
            impresion.producto.save()
            impresion.save()
            modelo = Modelo()
            modelo.name = 'Unico'
            modelo.scale_x = 100
            modelo.scale_y = 100
            modelo.scale_z = 100
            modelo.save()
            detalle_imp = DetalleImpresion()
            detalle_imp.print = impresion
            detalle_imp.modelo = modelo
            detalle_imp.quantity = 1
            detalle_imp.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super(ProductoCreateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        context['title'] = 'Nuevo Producto'
        context['action_button'] = 'Crear Producto'
        return context

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'administracion/specific/Producto/producto_edit.html'
    success_url = reverse_lazy('administracion:productos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Producto'
        context['action_button'] = 'Guardar Cambios'
        return context

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'administracion/specific/Producto/producto_delete.html'
    success_url = reverse_lazy('administracion:productos')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar producto'
        return context
