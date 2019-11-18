from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index_salida"),
    # Class Recinto
    path('crear_recinto/', RecintoCreate.as_view(), name="crear_recinto"),
    path('listar_recinto/', RecintoList.as_view(), name="listar_recinto"),
    path('editar_recinto/<int:pk>/', EditarRecinto, name="editar_recinto"),
    path('recinto_activar/<int:pk>/', RecintoActivar, name="recinto_activar"),
    path('recinto_desactivar/<int:pk>/', RecintoDesactivar, name="recinto_desactivar"),
    # Class Funcionario
    path('funcionarios/', FuncionarioList.as_view(), name='funcionario_list'),
    path('funcionarios/view/<int:pk>', FuncionarioView.as_view(), name='funcionario_view'),
    path('funcionarios/', FuncionarioCreate.as_view(), name='funcionario_new'),
    path('funcionarios/view/<int:pk>', FuncionarioView.as_view(), name='funcionario_view'),
    path('funcionarios/edit/<int:pk>', EditarFuncionario, name='funcionario_edit'),
    path('funcionario_activar/<int:pk>/', FuncionarioActivar, name="funcionario_activar"),
    path('funcionario_desactivar/<int:pk>/', FuncionarioDesactivar, name="funcionario_desactivar"),
    # Class Salida
    path('salida/', SalidasList, name="salidas_list"),
    path('Prestamo/', Prestamos, name="prestamos_list"),
    path('salida/view/<int:pk>', SalidasView.as_view(), name='salidas_view'),
    path('salida/detallesalidas/<int:pk>/', SalidasInfo.as_view(), name= "salidas_detalle"),
    path('salida/detalleprestamos/<int:pk>/', PrestamosInfo.as_view(), name="salidas_detalle"),
    path('salida/create', SalidasCreate.as_view(), name="salidas_create"),
    path('salida/update/<int:pk>/', SalidasUpdate.as_view(), name="salidas_update"),
    path('salida/delete/<int:pk>/', SalidasDelete.as_view(), name="salidas_delete"),

    path('ventas/buscar', VentaBuscar, name='venta_buscar'),   

    path('producto-list-ajax', ProductoListAjax, name="producto_list_ajax"),
    path('producto-view-ajax/<int:pk>/', ProductoViewAjax, name="producto_view_ajax"), 
]