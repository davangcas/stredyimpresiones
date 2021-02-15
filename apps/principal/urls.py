from django.urls import path

from apps.principal.views.index import IndexView
from apps.principal.views.about import AboutView
from apps.principal.views.producto import *

app_name = 'principal'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('acerca_de/', AboutView.as_view(), name="about"),
    path('producto/<int:pk>/', ProductoDetalleView.as_view(), name="producto_detalle"),
    path('catalogo/', ProductosListView.as_view(), name="catalogo"),
]