from django.urls import path
from . import views

from .views import ProveedorList, ProveedorCreate, ProveedorUpdate, ProveedorDelete, ProveedorSoftDelete, ProveedorActivar


urlpatterns = [
    path('index/', views.index, name="index_adquisiciones"),

    path('proveedor/', ProveedorList.as_view(), name="listar_proveedor"),
    path('proveedor/create', ProveedorCreate.as_view(), name="adquisiciones_proveedor_create"),
    path('proveedor/update/<int:pk>/', ProveedorUpdate.as_view(), name="adquisiciones_proveedor_update"),
    path('proveedor/softdelete/<int:pk>/', ProveedorSoftDelete.as_view(), name="adquisiciones_proveedor_soft_delete"),
    path('proveedor/activar/<int:pk>/', ProveedorActivar.as_view(), name="adquisiciones_proveedor_activar"),
    path('proveedor/delete/<int:pk>/', ProveedorDelete.as_view(), name="adquisiciones_proveedor_delete"),
]
