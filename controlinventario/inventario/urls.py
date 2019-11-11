from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index_inventario"),
    # Clase Categoria
    path('crear_categoria/', CrearCategoria.as_view(), name="crear_categoria"),
    path('listar_categoria/', ListarCategoria.as_view(), name="listar_categoria"),
    path('editar_categoria/<int:pk>/', EditarCategoria, name="editar_categoria"),
    path('categoria_activar/<int:pk>/', CategoriaActivar, name="categoria_activar"),
    path('categoria_desactivar/<int:pk>/', CategoriaDesactivar, name="categoria_desactivar"),
    # Clase Producto
    path('crear_producto/', CrearProducto.as_view(), name="crear_producto"),
    path('listar_producto/', ListarProducto.as_view(), name="listar_producto"),
    path('editar_producto/<int:pk>/', EditarProducto.as_view(), name="editar_producto"),
    path('mostrar_producto/<int:pk>/', MostrarProducto.as_view(), name="mostrar_producto"),
    path('editar_stock/', EditarStock, name="editar_stock"),
    path('editar_merma/', EditarMerma, name="editar_merma"),
    path('resetear_merma/<int:pk>/', ResetearMerma, name="resetear_merma"),
    path('producto_activar/<int:pk>/', ProductoActivar, name="producto_activar"),
    path('producto_desactivar/<int:pk>/', ProductoDesactivar, name="producto_desactivar"),
    # Estadistica
    path('estadistica/', MostrarEstadistica, name="listar_estadistica"),
]
