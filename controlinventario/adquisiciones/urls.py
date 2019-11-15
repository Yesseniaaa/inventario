from django.urls import path
from . import views

from .views import IngresoList, IngresoCreate, IngresoUpdate, IngresoDelete
from .views import ProveedorList, ProveedorCreate, ProveedorUpdate, ProveedorDelete, ProveedorSoftDelete, ProveedorActivar
from .views import OrdenAdqList, OrdenAdqCreate, OrdenAdqUpdate, OrdenAdqState, OrdenAdqInfo
from .views import ProductoCreate, ProductoViewAjax, ProductoListAjax, ProductoCreateAjax


urlpatterns = [
    path('index/', views.index, name="index_adquisiciones"),


    #path('ingreso/', IngresoList.as_view(), name="adquisiciones_ingresos"),
    #path('ingreso/create', IngresoCreate.as_view(), name="adquisiciones_ingresos_create"),
    #path('ingreso/update/<int:pk>/', IngresoUpdate.as_view(), name="adquisiciones_ingresos_update"),
    #path('ingreso/delete/<int:pk>/', IngresoDelete.as_view(), name="adquisiciones_ingresos_delete"),

    path('proveedor/', ProveedorList.as_view(), name="adquisiciones_proveedores"),
    path('proveedor/create', ProveedorCreate.as_view(), name="adquisiciones_proveedor_create"),
    path('proveedor/update/<int:pk>/', ProveedorUpdate.as_view(), name="adquisiciones_proveedor_update"),
    path('proveedor/softdelete/<int:pk>/', ProveedorSoftDelete.as_view(), name="adquisiciones_proveedor_soft_delete"),
    path('proveedor/activar/<int:pk>/', ProveedorActivar.as_view(), name="adquisiciones_proveedor_activar"),
    path('proveedor/delete/<int:pk>/', ProveedorDelete.as_view(), name="adquisiciones_proveedor_delete"),

    path('orden_adquisicion/', OrdenAdqList, name="adquisiciones_ordenes_adquisiciones"),
    path('orden_adquisicion/create', OrdenAdqCreate.as_view(), name="adquisiciones_ordenes_create"),
    path('orden_adquisicion/update/<int:pk>/', OrdenAdqUpdate.as_view(), name="adquisiciones_ordenes_update"),
    path('orden_adquisicion/state/<int:pk>/', OrdenAdqState.as_view(), name="adquisiciones_ordenes_state"),
    path('orden_adquisicion/info/<int:pk>/', OrdenAdqInfo.as_view(), name="adquisiciones_ordenes_info"),

    #path('orden_adquisicion/delete/<int:pk>/', OrdenAdqDelete.as_view(), name="adquisiciones_ordenes_delete"),

    path('producto/create', ProductoCreate.as_view(), name="adquisiciones_producto"),
    path('producto/create-ajax', ProductoCreateAjax, name="adquisiciones_producto_create_ajax"),
    path('producto-list-ajax', ProductoListAjax , name="producto_list_ajax"),
    path('producto-view-ajax/<int:pk>/', ProductoViewAjax , name="producto_view_ajax"),


]
