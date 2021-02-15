from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseRedirect

from apps.administracion.models import Cliente
from apps.administracion.Views.Cliente.forms import ClienteForm

class ClienteListView(ListView):
    model = Cliente
    template_name = 'administracion/specific/Cliente/cliente_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Clientes'
        context['title_table'] = 'Clientes'
        context['table_id'] = 'Clientes'
        context['table_fields'] = [
            'Nombre',
            'Teléfono',
            'Descripción',
            'Acciones',
        ]
        context['add_button_name'] = 'Nuevo Cliente'
        return context

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'administracion/specific/Cliente/cliente_new.html'
    success_url = reverse_lazy('administracion:clientes')
    
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
        context['title'] = 'Agregar Cliente'
        context['action_button'] = 'Agregar Nuevo Cliente'
        return context

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'administracion/specific/Cliente/cliente_new.html'
    success_url = reverse_lazy('administracion:clientes')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['action_button'] = 'Guardar Cambios'
        return context
