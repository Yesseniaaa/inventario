from django.urls import path
from . import views

from .views import IngresoList, IngresoCreate, IngresoUpdate, IngresoDelete
from .views import PrestamoList, PrestamoCreate, PrestamoInfo, PrestamoUpdate, PrestamoState
from .views import UsuarioList, UsuarioCreate, UsuarioUpdate, UsuarioSoftDelete, UsuarioActivar
from .views import ProductoCreate, ProductoViewAjax, ProductoListAjax, ProductoCreateAjax

urlpatterns = [
    path('index/', views.index, name="index_adquisiciones"),


    path('prestamo/', PrestamoList, name="adquisiciones_ordenes_adquisiciones"),
    path('prestamo/create', PrestamoCreate.as_view(), name="adquisiciones_ordenes_create"),
    path('prestamo/update/<int:pk>/', PrestamoUpdate.as_view(), name="adquisiciones_ordenes_update"),
    path('prestamo/state/<int:pk>/', PrestamoState.as_view(), name="adquisiciones_ordenes_state"),
    path('prestamo/info/<int:pk>/', PrestamoInfo.as_view(), name="adquisiciones_ordenes_info"),

    #path('orden_adquisicion/delete/<int:pk>/', OrdenAdqDelete.as_view(), name="adquisiciones_ordenes_delete"),

    path('usuario/', UsuarioList.as_view(), name="listar_usuario"),
    path('usuario/create', UsuarioCreate.as_view(), name="adquisiciones_usuario_create"),
    path('usuario/update/<int:pk>/', UsuarioUpdate.as_view(), name="adquisiciones_usuario_update"),
    path('usuario/softdelete/<int:pk>/', UsuarioSoftDelete.as_view(), name="adquisiciones_usuario_soft_delete"),
    path('usuario/activar/<int:pk>/', UsuarioActivar.as_view(), name="adquisiciones_usuario_activar"),

    path('producto/create', ProductoCreate.as_view(), name="adquisiciones_producto"),
    path('producto/create-ajax', ProductoCreateAjax, name="adquisiciones_producto_create_ajax"),
    path('producto-list-ajax', ProductoListAjax , name="producto_list_ajax"),
    path('producto-view-ajax/<int:pk>/', ProductoViewAjax , name="producto_view_ajax"),
]
