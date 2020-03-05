from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import Activofijo
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from salidas.models import Recinto, Funcionario
from datetime import date
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
today = date.today() #fecha actual


class CrearActivofijo(SuccessMessageMixin, CreateView):
    model = Activofijo
    form_class = ActivofijoForm
    template_name = 'activofijo/crear_activofijo.html'
    success_url = reverse_lazy('crear_activofijo')
    success_message = "El Activo Fijo fue creado con éxito."

def ListarActivofijo(request):
    activosfijos = Activofijo.objects.all()
    print (activosfijos)
    context = {'activosfijos':activosfijos}
    return render(request,'activofijo/listar_activofijo.html', context)

def EditarActivofijo(request,pk):
    activofijo = Activofijo.objects.get(id=pk)
    if request.method == 'GET':
        form = ActivofijoForm(instance=activofijo)
    else:
        form = ActivofijoForm(request.POST, instance=activofijo)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha actualizado correctamente el activofijo " + activofijo.nombre + ".")
        return redirect('listar_activofijo')
    return render(request, 'activofijo/editar_activofijo.html', {'form':form, 'activofijo':activofijo})

def ActivofijoActivar(request,pk):
    activofijo = Activofijo.objects.get(id=pk)
    activofijo.estado = True
    activofijo.save()
    return redirect('listar_activofijo')

def ActivofijoDesactivar(request,pk):
    activofijo = Activofijo.objects.get(id=pk)
    activofijo.estado = False
    activofijo.save()
    return redirect('listar_activofijo')