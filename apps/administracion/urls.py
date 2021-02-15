from django.urls import path
from django.contrib.auth.views import LogoutView

from apps.administracion.Views.Cliente.views import *
from apps.administracion.Views.Producto.views import *
from apps.administracion.Views.Pedido.views import *
from apps.administracion.Views.Caja.views import *
from apps.administracion.Views.Datos.views import *
from apps.administracion.Views.Material.views import *
from apps.administracion.Views.Impresion.views import *
from apps.administracion.Views.Modelos.views import *
from apps.administracion.Views.Login.views import LoginFormView, CambiarPassword
from apps.administracion.Views.Index.views import IndexView
from apps.administracion.Views.Admins.views import *
from apps.administracion.Views.Publicacion.views import *
from apps.administracion.Views.CostoExtra.views import *

app_name = 'administracion'

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('cambiar_contrasseña/', CambiarPassword.as_view(), name="password_change"),
    path('logout/', LogoutView.as_view(next_page='administracion:login'), name="logout"),
    path('clientes/', ClienteListView.as_view(), name="clientes"),
    path('inicio/', IndexView.as_view(), name="index"),
    path('cliente/nuevo', ClienteCreateView.as_view(), name="clientes_new"),
    path('clientes/editar/<int:pk>/', ClienteUpdateView.as_view(), name="clientes_edit"),
    path('productos/', ProductoListView.as_view(), name="productos"),
    path('productos/nuevo/', ProductoCreateView.as_view(), name="productos_new"),
    path('productos/editar/<int:pk>/', ProductoUpdateView.as_view(), name="productos_edit"),
    path('productos/eliminar/<int:pk>/', ProductoDeleteView.as_view(), name="productos_eliminar"),
    path('productos/impresiones/nuevo/<int:pk>/', ImpresionCreate.as_view(), name="impresion_new"),
    path('productos/impresiones/<int:pk>/', ImpresionList.as_view(), name="impresiones"),
    path('productos/impresiones/editar/<int:pk>', ImpresionUpdate.as_view(), name="impresion_edit"),
    path('productos/impresiones/eliminar/<int:pk>', ImpresionDelete.as_view(), name="impresion_delete"),
    path('productos/impresiones/modelos/nuevo/<int:pk>/', ModeloCreate.as_view(), name="modelo_new"),
    path('productos/impresiones/modelos/eliminar/<int:pk>/', ModeloDelete.as_view(), name="modelo_delete"),
    path('productos/impresion/modelos/<int:pk>', ModeloList.as_view(), name="modelos"),
    path('pedidos/', PedidoList.as_view(), name="pedidos"),
    path('pedidos/nuevo/', PedidoCreate.as_view(), name="pedidos_new"),
    path('pedidos/nuevo/<int:pk>/', PedidoClienteCreate.as_view(), name="pedidos_cliente_new"),
    path('pedidos/agregar/<int:pk>', PedidoProductoAgregar.as_view(), name="pedido_agregar_producto"),
    path('pedidos/detalle/<int:pk>', PedidoDetalleList.as_view(), name="pedidos_detalle"),
    path('pedidos/detalle/impresiones/<int:pk>', ImpresionesRealizarList.as_view(), name="impresiones_detalle"),
    path('pedidos/detalle/impresion/editar/<int:pk>/', ImpresionDetalleUpdate.as_view(), name="impresion_detalle_edit"),
    path('pedidos/impresiones/', ImpresionPedidoTodas.as_view(), name="pedidos_impresiones_realizar"),
    path('pedidos/impresiones/detalle/<int:pk>/', ImpresionDetalleVer.as_view(), name="pedidos_impresiones_ver"),
    path('pedidos/impresion/cambiar_estado/<int:id>/', impresion_cambio, name="impresion_cambio"),
    path('pedidos/impresion/cancelar/<int:id>/', impresion_cancelar, name="impresion_cancelar"),
    path('pedidos/pagado/<int:id>/', pedido_pagado, name="pedidos_pagado"),
    path('pedidos/cancelado/<int:id>/', pedido_cancelado, name="pedidos_cancelado"),
    path('caja/registro/nuevo/', RegistroCreate.as_view(), name="registro_new"),
    path('caja/movimientos/', CajaList.as_view(), name="caja_movimientos"),
    path('caja/extraccion/', ExtraccionCreate.as_view(), name="extraccion"),
    path('caja/gastos/', GastosListView.as_view(), name="gastos"),
    path('caja/gastos/nuevo/', GastosCreateView.as_view(), name="gastos_new"),
    path('caja/gastos/editar/<int:pk>/', GastosUpdateView.as_view(), name="gastos_edit"),
    path('caja/gastos/eliminar/<int:pk>/', GastosDeleteView.as_view(), name="gastos_delete"),
    path('datos/editar/', DatosCreateView.as_view(), name="datos_edit"),
    path('datos/detalle/', DatosListView.as_view(), name="datos_detail"),
    path('insumos/materiales/', MaterialListView.as_view(), name="materiales"),
    path('insumos/materiales/nuevo/', MaterialCreateView.as_view(), name="materiales_new"),
    path('insumos/materiales/editar/<int:pk>/', MaterialUpdateView.as_view(), name="materiales_edit"),
    path('insumos/colores/', ColorListView.as_view(), name="colores"),
    path('insumos/colores/nuevo/', ColorCreateView.as_view(), name="colores_new"),
    path('insumos/colores/editar/<int:pk>/', ColorUpdate.as_view(), name="colores_edit"),
    path('insumos/colores/eliminar/<int:pk>/', ColorDelete.as_view(), name="colores_delete"),
    path('insumos/colores/nuevo_rollo/<int:id>/', nuevo_rollo, name="nuevo_rollo"),
    path('productos/impresiones/modelos/editar/<int:pk>/', ModeloUpdate.as_view(), name="modelo_edit"),
    path('administradores/', AdministratorList.as_view(), name="administradores"),
    path('administradores/nuevo/', AdministratorCreate.as_view(), name="administradores_new"),
    path('administradores/eliminar/<int:pk>/', AdministratorDelete.as_view(), name="administradores_delete"),
    path('administradores/actualizar/<int:pk>/', AdministratorUpdate.as_view(), name="administradores_edit"),
    path('publicaciones/', PublicacionListView.as_view(), name="publicaciones"),
    path('publicaciones/nueva/', PublicacionCreateView.as_view(), name="publicacion_new"),
    path('publicaciones/eliminar/<int:pk>/', PublicacionDeleteView.as_view(), name="publicacion_delete"),
    path('publiaciones/editar/<int:pk>/', PubliacionUpdateView.as_view(), name="publicacion_edit"),
    path('productos/impresiones/nuevo/costo/<int:pk>/', CostoExtraCreateView.as_view(), name="new_costo_extra"),
    path('productos/impresiones/costos/eliminar/<int:pk>/', CostoExtraDeleteView.as_view(), name="delete_costo_extra"),
    path('productos/impresiones/costo/editar/<int:pk>/', CostoExtraUpdate.as_view(), name="edit_costo_extra")
]