from django.views.generic import TemplateView

from apps.principal.models.publication import Publication

class IndexView(TemplateView):
    template_name = 'principal/specific/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blaster Impresiones 3D'
        context['publicacion'] = Publication.objects.all().order_by('-id')[:12]
        return context