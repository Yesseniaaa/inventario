from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .models import Activofijo

today = date.today()  # fecha actual


class CrearActivofijo(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    model = Activofijo
    form_class = ActivofijoForm
    template_name = "activofijo/crear_activofijo.html"
    success_url = reverse_lazy("crear_activofijo")
    success_message = "El Activo Fijo fue creado con éxito."


@login_required()
def ListarActivofijo(request):
    activosfijos = Activofijo.objects.all()
    context = {"activosfijos": activosfijos}
    return render(request, "activofijo/listar_activofijo.html", context)


@login_required()
def EditarActivofijo(request, pk):
    activofijo = Activofijo.objects.get(id_activo=pk)
    if request.method == "GET":
        form = ActivofijoForm(instance=activofijo)
    else:
        form = ActivofijoForm(request.POST, instance=activofijo)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Se ha actualizado correctamente el activofijo " + activofijo.nombre + "."
            )
        return redirect("listar_activofijo")
    return render(
        request, "activofijo/editar_activofijo.html", {"form": form, "activofijo": activofijo}
    )


@login_required()
def ActivofijoActivar(request, pk):
    activofijo = Activofijo.objects.get(id_activo=pk)
    activofijo.estado = True
    activofijo.save()
    return redirect("listar_activofijo")


@login_required()
def ActivofijoDesactivar(request, pk):
    activofijo = Activofijo.objects.get(id_activo=pk)
    activofijo.estado = False
    activofijo.save()
    return redirect("listar_activofijo")
