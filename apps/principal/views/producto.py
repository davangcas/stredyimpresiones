from django.views.generic import ListView, TemplateView

from apps.principal.models.publication import Publication

class ProductoDetalleView(TemplateView):
    template_name = "principal/specific/catalogo/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Publication.objects.get(pk=self.kwargs['pk']).title
        context['publicacion'] = Publication.objects.get(pk=self.kwargs['pk'])
        return context

class ProductosListView(TemplateView):
    template_name = "principal/specific/catalogo/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Catálogo de productos"
        context['productos'] = Publication.objects.all().order_by('-id')
        return context
