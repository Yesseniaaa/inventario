from django.urls import path
from .views import *

urlpatterns = [
    path('crear_activofijo/', CrearActivofijo.as_view(), name="crear_activofijo"),
    path('listar_activofijo/', ListarActivofijo, name="listar_activofijo"),
    path('editar_activofijo/<int:pk>/', EditarActivofijo, name="editar_activofijo"),
    path('activofijo_activar/<int:pk>/', ActivofijoActivar, name="activofijo_activar"),
    path('activofijo_desactivar/<int:pk>/', ActivofijoDesactivar, name="activofijo_desactivar"),
]