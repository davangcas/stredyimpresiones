from django.views.generic import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from apps.administracion.models import CostoExtra, Producto
from apps.administracion.Views.CostoExtra.forms import CostoExtraForm

class CostoExtraCreateView(CreateView):
    model = CostoExtra
    template_name = "administracion/specific/CostoExtra/create.html"
    form_class = CostoExtraForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('administracion:impresiones', kwargs={'pk':self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            costo = form.save(commit=False)
            producto = Producto.objects.get(pk=self.kwargs['pk'])
            costo.product = producto
            producto.price = producto.price + costo.amount
            producto.save()
            costo.save()
            mismos_costos = CostoExtra.objects.filter(concept=costo.concept)
            for c in mismos_costos:
                product = Producto.objects.get(pk=c.product.id)
                valor = c.amount
                c.amount = costo.amount
                product.price = product.price - valor + costo.amount
                product.save()
                c.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = None
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Nuevo Costo"
        context['action_button'] = "Agregar Costo"
        return context

class CostoExtraDeleteView(DeleteView):
    model = CostoExtra
    template_name = "administracion/specific/CostoExtra/delete.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('administracion:impresiones', kwargs={'pk':self.object.product.id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        producto = Producto.objects.get(pk=self.object.product.id)
        producto.price = producto.price - self.object.amount
        producto.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eliminar costo"
        return context

class CostoExtraUpdate(UpdateView):
    model = CostoExtra
    form_class = CostoExtraForm
    template_name = "administracion/specific/CostoExtra/update.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('administracion:impresiones', kwargs={'pk':CostoExtra.objects.get(pk=self.kwargs['pk']).product.id})

    def form_valid(self, form):
        costo = CostoExtra.objects.get(pk=self.kwargs['pk'])
        valor = costo.amount
        self.object = form.save()
        producto = Producto.objects.get(pk=self.object.product.id)
        producto.price = producto.price - valor + self.object.amount
        producto.save()
        mismos_costos = CostoExtra.objects.filter(concept=self.object.concept)
        for c in mismos_costos:
            product = Producto.objects.get(pk=c.product.id)
            product.price = product.price - valor + self.object.amount
            c.amount = self.object.amount
            product.save()
            c.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Costo"
        context['action_button'] = "Editar Costo"
        return context
