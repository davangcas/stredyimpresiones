from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "principal/specific/acerca_de/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blaster - Acerca de nosotros'
        return context