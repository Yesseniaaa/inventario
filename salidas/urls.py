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
    path('funcionario/', FuncionarioList, name='funcionario_list'),
    path('funcionario/view/<int:pk>', FuncionarioView.as_view(), name='funcionario_view'),
    path('funcionario/new', FuncionarioCreate.as_view(), name='funcionario_new'),
    path('funcionario/view/<int:pk>', FuncionarioView.as_view(), name='funcionario_view'),
    path('funcionario/edit/<int:pk>', EditarFuncionario, name='editar_funcionario'),
    path('funcionario_activar/<int:pk>/', FuncionarioActivar, name="funcionario_activar"),
    path('funcionario_desactivar/<int:pk>/', FuncionarioDesactivar, name="funcionario_desactivar"),
    # Class Salida
    path('salidas_list/', SalidasList, name="salidas_list"),
    path('salidas_list/<int:pk>', SalidasView.as_view(), name='salidas_view'),
    path('salidas_detalle/<int:pk>/', SalidasInfo.as_view(), name= "salidas_detalle"),
    path('salidas_create/', SalidasCreate.as_view(), name="salidas_create"),
    path('salidas_update/<int:pk>/', SalidasUpdate.as_view(), name="salidas_update"),
    path('salidas_delete/<int:pk>/', SalidasDelete.as_view(), name="salidas_delete"),
    #Class Prestamo
    path('prestamos_list/', PrestamosList, name="prestamos_list"),
    path('prestamos_view/<int:pk>', PrestamosView.as_view(), name='prestamos_view'),
    path('prestamos_detalle/<int:pk>/', PrestamosInfo.as_view(), name= "prestamos_detalle"),
    path('prestamos_create/', PrestamosCreate.as_view(), name="prestamos_create"),
    path('prestamos_update/<int:pk>/', PrestamosUpdate.as_view(), name="prestamos_update"),
    path('prestamos_delete/<int:pk>/', PrestamosDelete.as_view(), name="prestamos_delete"),
    
    path('salida/buscar', SalidaBuscar, name='salida_buscar'), 
    path('prestamo/buscar', PrestamoBuscar, name='prestamo_buscar'),    

    path('producto-list-ajax', ProductoListAjax, name="producto_list_ajax"),
    path('producto-view-ajax/<int:pk>/', ProductoViewAjax, name="producto_view_ajax"), 
]