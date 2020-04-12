from django.urls import path

from . import views
from .views import OrdenAdqList, OrdenAdqUpdate, OrdenAdqState, OrdenAdqInfo, OrdenAdqCreateInvoce, \
    OrdenAdqCreateReturn, DevolucionList, SelectView, DetalleDevolucion, EditarDevolucion
from .views import ProductoCreate, ProductoViewAjax, ProductoListAjax, ProductoCreateAjax
from .views import ProveedorList, ProveedorCreate, ProveedorUpdate, ProveedorDelete, ProveedorSoftDelete, \
    ProveedorActivar

urlpatterns = [
    path('index/', views.index, name="index_adquisiciones"),

    # path('ingreso/', IngresoList.as_view(), name="adquisiciones_ingresos"),
    # path('ingreso/create', IngresoCreate.as_view(), name="adquisiciones_ingresos_create"),
    # path('ingreso/update/<int:pk>/', IngresoUpdate.as_view(), name="adquisiciones_ingresos_update"),
    # path('ingreso/delete/<int:pk>/', IngresoDelete.as_view(), name="adquisiciones_ingresos_delete"),

    path('proveedor/', ProveedorList.as_view(), name="adquisiciones_proveedores"),
    path('proveedor/create', ProveedorCreate.as_view(), name="adquisiciones_proveedor_create"),
    path('proveedor/update/<int:pk>/', ProveedorUpdate.as_view(), name="adquisiciones_proveedor_update"),
    path('proveedor/softdelete/<int:pk>/', ProveedorSoftDelete.as_view(), name="adquisiciones_proveedor_soft_delete"),
    path('proveedor/activar/<int:pk>/', ProveedorActivar.as_view(), name="adquisiciones_proveedor_activar"),
    path('proveedor/delete/<int:pk>/', ProveedorDelete.as_view(), name="adquisiciones_proveedor_delete"),

    path('orden_adquisicion/', OrdenAdqList, name="adquisiciones_ordenes_adquisiciones"),
    path('orden_adquisicion/select', SelectView.as_view(), name="adquisiciones_selector"),
    path('orden_adquisicion/devoluciones', DevolucionList.as_view(), name="adquisiciones_ordenes_devoluciones"),
    path('orden_adquisicion/devoluciones/<int:pk>/', DetalleDevolucion.as_view(), name="adquisiciones_ordenes_devoluciones"),
    path('orden_adquisicion/devoluciones/editar/<int:pk>/', EditarDevolucion.as_view(), name="adquisiciones_ordenes_devoluciones_edit"),
    path('orden_adquisicion/create/factura', OrdenAdqCreateInvoce.as_view(),
         name="adquisiciones_ordenes_create_factura"),
    path('orden_adquisicion/create/devolucion', OrdenAdqCreateReturn.as_view(),
         name="adquisiciones_ordenes_create_devolucion"),
    path('orden_adquisicion/update/<int:pk>/', OrdenAdqUpdate.as_view(), name="adquisiciones_ordenes_update"),
    path('orden_adquisicion/state/<int:pk>/', OrdenAdqState.as_view(), name="adquisiciones_ordenes_state"),
    path('orden_adquisicion/info/<int:pk>/', OrdenAdqInfo.as_view(), name="adquisiciones_ordenes_info"),

    # path('orden_adquisicion/delete/<int:pk>/', OrdenAdqDelete.as_view(), name="adquisiciones_ordenes_delete"),

    path('producto/create', ProductoCreate.as_view(), name="adquisiciones_producto"),
    path('producto/create-ajax', ProductoCreateAjax, name="adquisiciones_producto_create_ajax"),
    path('producto-list-ajax', ProductoListAjax, name="producto_list_ajax"),
    path('producto-view-ajax/<int:pk>/', ProductoViewAjax, name="producto_view_ajax"),
]
