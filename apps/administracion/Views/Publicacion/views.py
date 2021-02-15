from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from apps.principal.models.publication import Publication
from apps.administracion.Views.Publicacion.forms import PublicacionForm

class PublicacionCreateView(CreateView):
    model = Publication
    template_name = "administracion/specific/Publicacion/create.html"
    form_class = PublicacionForm
    success_url = reverse_lazy('administracion:publicaciones')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Nueva Publicación"
        context['action_button'] = 'Crear Publicación'
        return context

class PublicacionListView(ListView):
    model = Publication
    template_name = "administracion/specific/Publicacion/list.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Publicaciones'
        context['title_table'] = 'Lista de Publicaciones'
        context['table_id'] = 'Publicaciones'
        context['table_fields'] = [
            'ID',
            'Fecha de publicación',
            'Título',
            'Producto',
            'Imágen',
            'Acciones',
        ]
        context['add_button_name'] = 'Nueva Publicación'
        return context
    
class PublicacionDeleteView(DeleteView):
    model = Publication
    template_name = "administracion/specific/Publicacion/delete.html"
    success_url = reverse_lazy('administracion:publicaciones')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar publicación'
        return context

class PubliacionUpdateView(UpdateView):
    model = Publication
    template_name = "administracion/specific/Publicacion/update.html"
    success_url = reverse_lazy('administracion:publicaciones')
    form_class = PublicacionForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Publicación"
        context['action_button'] = 'Modificar Publicación'
        return context
