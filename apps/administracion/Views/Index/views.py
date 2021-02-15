from datetime import datetime as dt

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from apps.administracion.models import Cliente, Producto, Caja, Pedido


class IndexView(TemplateView):
    template_name = 'administracion/specific/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio'
        context['count_clients'] = Cliente.objects.all().count()
        context['productos'] = Producto.objects.all().count()
        context['productos_hoy'] = Producto.objects.filter(date_created__year=dt.now().year, date_created__month=dt.now().month, date_created__day=dt.now().day).count()
        context['caja'] = Caja.objects.last()
        context['pedidos'] = Pedido.objects.filter(date_created__year=dt.now().year, date_created__month=dt.now().month, date_created__day=dt.now().day).count()
        return context
