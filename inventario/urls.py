from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index_inventario"),
    # Clase Categoria
    path("crear_categoria/", CrearCategoria.as_view(), name="crear_categoria"),
    path("listar_categoria/", ListarCategoria.as_view(), name="listar_categoria"),
    path("editar_categoria/<int:pk>/", EditarCategoria, name="editar_categoria"),
    path("categoria_activar/<int:pk>/", CategoriaActivar, name="categoria_activar"),
    path("categoria_desactivar/<int:pk>/", CategoriaDesactivar, name="categoria_desactivar"),
    # Clase Producto
    path("listar_producto/", ListarProducto.as_view(), name="listar_producto"),
    path("listar_merma/", ListarMerma.as_view(), name="listar_merma"),
    path("listar_cat_prod/<int:pk>/", ListarCatProd, name="listar_cat_prod"),
    path("editar_producto/<int:pk>/", EditarProducto.as_view(), name="editar_producto"),
    path("mostrar_producto/<int:pk>/", MostrarProducto.as_view(), name="mostrar_producto"),
    path("historial_precio/<int:pk>/", HistorialPrecio, name="historial_precio"),
    path("editar_stock/", EditarStock, name="editar_stock"),
    path("editar_merma/", EditarMerma.as_view(), name="editar_merma"),
    path("resetear_merma/<int:pk>/", ResetearMerma, name="resetear_merma"),
    path("producto_activar/<int:pk>/", ProductoActivar, name="producto_activar"),
    path("producto_desactivar/<int:pk>/", ProductoDesactivar, name="producto_desactivar"),
    # Estadistica
    path("estadistica/", MostrarEstadistica, name="listar_estadistica"),
    path("estadistica2/", MostrarEstadistica2, name="listar_estadistica2"),
    path("historial/get/<int:pk>", GetHistorialProducto, name="get_historial"),
]
