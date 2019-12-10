from django.shortcuts import render, redirect
from .form import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.contrib.messages.views import SuccessMessageMixin
import time
from django.utils import timezone

def index(request):
    return render(request,'salidas/index.html')

# Class Recinto

class RecintoCreate(SuccessMessageMixin, CreateView):
    model = Recinto
    form_class = RecintoForm
    template_name = 'salidas/crear_recinto.html'
    success_url = reverse_lazy('crear_recinto')
    success_message = "El recinto fue creado con éxito."

class RecintoList(ListView):
    model = Recinto
    template_name = 'salidas/listar_recinto.html'

def EditarRecinto(request,pk):
    recinto = Recinto.objects.get(id=pk)
    if request.method == 'GET':
        form = RecintoForm(instance=recinto)
    else:
        form = RecintoForm(request.POST, instance=recinto)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha actualizado correctamente el recinto " + recinto.nombre + ".")
        return redirect('listar_recinto')
    return render(request, 'salidas/editar_recinto.html', {'form':form, 'recinto':recinto})

def RecintoActivar(request,pk):
    recinto = Recinto.objects.get(id=pk)
    recinto.estado = True
    recinto.save()
    return redirect('listar_recinto')

def RecintoDesactivar(request,pk):
    recinto = Recinto.objects.get(id=pk)
    recinto.estado = False
    recinto.save()
    return redirect('listar_recinto')

# Class Funcionario

def FuncionarioList(request):
    funcionarios = Funcionario.objects.all()
    context = {'funcionarios':funcionarios}
    return render(request, 'salidas/funcionario_list.html', context)

class FuncionarioView(DetailView):
    model = Funcionario
    template_name = 'salidas/funcionario_detail.html'

class FuncionarioCreate(CreateView):
    model = Funcionario
    form_class = FuncionarioForm
    success_url = reverse_lazy('funcionario_list')
    template_name = 'salidas/funcionario_form.html'

def EditarFuncionario(request,pk):
    funcionario = Funcionario.objects.get(id=pk)
    if request.method == 'GET':
        form = FuncionarioForm(instance=funcionario)
    else:
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha actualizado correctamente el funcionario " + funcionario.nombre + ".")
        return redirect('listar_funcionario')
    return render(request, 'salida/editar_funcionario.html', {'form':form, 'funcionario':funcionario})

def FuncionarioActivar(request,pk):
    funcionario = Funcionario.objects.get(id=pk)
    funcionario.estado = True
    funcionario.save()
    return redirect('listar_funcionario')

def FuncionarioDesactivar(request,pk):
    funcionario = Funcionario.objects.get(id=pk)
    funcionario.estado = False
    funcionario.save()
    return redirect('listar_funcionario')

# Class Salida

class SalidasCreate(CreateView):
    model = Salida
    form_class = SalidaForm
    template_name = 'salidas/salidas_form.html'
    success_url = reverse_lazy('salidas_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            salida = form.save()
            productos_id = request.POST.getlist('productos_ids')
            productos_value = request.POST.getlist('productos_precio')
            productos_cantidad = request.POST.getlist('productos_cantidad')
            for count, producto in enumerate(productos_id, start=0):
                if (productos_cantidad[count] != '' and productos_value[count] != 0) or (productos_cantidad[count] != '' and productos_cantidad[count] != 0):
                    Ven_prod.objects.create(id_prod_id=producto, id_salida_id=salida.id,precio=productos_value[count], cantidad=productos_cantidad[count])
        return redirect(reverse('salidas_create'))

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        productos = Producto.objects.all()
        return render(request, self.template_name, {'form': form, 'productos': productos})


class SalidasView(DetailView):
    model = Sal_prod
    template_name = 'salidas/salidas_detail.html'


def SalidasList(request):
    salidas = Salida.objects.all()
    context = {'salidas':salidas}
    return render(request,'salidas/salidas_list.html', context)


class SalidasInfo(UpdateView):
    model = Salida
    form_class = SalidaForm
    template_name = 'salidas/salidas_info.html'
    success_url = reverse_lazy('salidas/salidas_list.html')

    def get(self, request, *args, **kwargs):
        salidas = self.model.objects.get(id=kwargs['pk'])
        sal_prod = Sal_prod.objects.filter(id_salida_id=salidas)

        form = self.form_class()
        return render(request, self.template_name,
                      {'salidas': salidas, 'sal_prod': sal_prod})


class SalidasUpdate(UpdateView):
    model = Salida
    form_class = SalidaForm
    success_url = reverse_lazy('salidas_list')
    template_name = 'salidas/salidas_form.html'

    def post(self, request, *args, **kwargs):
        salidas = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(request.POST, instance=salidas)
        if form.is_valid():
            salida = form.save()

            productos_id = request.POST.getlist('productos_ids')
            productos_value = request.POST.getlist('productos_precio')
            productos_cantidad = request.POST.getlist('productos_cantidad')

            for count, producto in enumerate(productos_id, start=0):
                if (productos_cantidad[count] != '' and productos_value[count] != 0) or (
                        productos_cantidad[count] != '' and productos_cantidad[count] != 0):
                    sal_prod = Sal_prod.objects.filter(id_salida_id=salida.id).filter(id_prod_id=producto)
                    if sal_prod:
                        sal_prod.update(precio=productos_value[count], cantidad=productos_cantidad[count])
                    else:
                        Sal_prod.objects.create(id_salida_id=salida.id, id_prod_id=producto,
                                                precio=productos_value[count], cantidad=productos_cantidad[count])
        return redirect(reverse('salidas_list'))

    def get(self, request, *args, **kwargs):
        salidas = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(instance=salidas)
        sal_prod = Sal_prod.objects.filter(id_salida=salidas)
        return render(request, self.template_name, {'form': form, 'sal_prod': sal_prod})


class SalidasDelete(DeleteView):
    model = Salida
    success_url = reverse_lazy('salidas_list')
    template_name = 'salidas/salidas_delete.html'


def SalidaBuscar(request):
    buscarsalida = Salida.objects.filter(estado=request.POST['estado'])
    context = {'object_list': buscarsalida}
    return render(request, 'salidas/salidas_list.html', context)

# Class Prestamo

class PrestamosCreate(CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'salidas/prestamos_form.html'
    success_url = reverse_lazy('prestamos_list')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            prestamo = form.save()
            productos_id = request.POST.getlist('productos_ids')
            productos_value = request.POST.getlist('productos_precio')
            productos_cantidad = request.POST.getlist('productos_cantidad')
            for count, producto in enumerate(productos_id, start=0):
                if (productos_cantidad[count] != '' and productos_value[count] != 0) or (
                        productos_cantidad[count] != '' and productos_cantidad[count] != 0):
                    print (Sal_prod.objects.create(id_prod_id=producto, id_prestamo_id=prestamo.id,
                                                   precio=productos_value[count], cantidad=productos_cantidad[count]))

        return redirect(reverse('prestamos_create'))

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        productos = Producto.objects.all()
        return render(request, self.template_name, {'form': form, 'productos': productos})


class PrestamosView(DetailView):
    model = Pre_prod
    template_name = 'salidas/prestamos_detail.html'

def PrestamosList(request):
    prestamos = Prestamo.objects.all()
    context = {'prestamos':prestamos}
    return render(request,'salidas/prestamos_list.html', context)


class PrestamosInfo(UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'salidas/prestamos_info.html'
    success_url = reverse_lazy('salidas/prestamos_list.html')

    def get(self, request, *args, **kwargs):
        prestamos = self.model.objects.get(id=kwargs['pk'])
        pre_prod = Pre_prod.objects.filter(id_prestamo_id=prestamos)

        form = self.form_class()
        return render(request, self.template_name,
                      {'prestamos': prestamos, 'pre_prod': pre_prod})


class PrestamosUpdate(UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    success_url = reverse_lazy('prestamos_list')
    template_name = 'salidas/prestamos_form.html'

    def post(self, request, *args, **kwargs):
        prestamos = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(request.POST, instance=prestamos)
        if form.is_valid():
            prestamo = form.save()

            productos_id = request.POST.getlist('productos_ids')
            productos_value = request.POST.getlist('productos_precio')
            productos_cantidad = request.POST.getlist('productos_cantidad')

            for count, producto in enumerate(productos_id, start=0):
                if (productos_cantidad[count] != '' and productos_value[count] != 0) or (
                        productos_cantidad[count] != '' and productos_cantidad[count] != 0):
                    pre_prod = Pre_prod.objects.filter(id_prestamo_id=prestamo.id).filter(id_prod_id=producto)
                    if pre_prod:
                        pre_prod.update(precio=productos_value[count], cantidad=productos_cantidad[count])
                    else:
                        Pre_prod.objects.create(id_prestamo_id=prestamo.id, id_prod_id=producto,
                                                precio=productos_value[count], cantidad=productos_cantidad[count])
        return redirect(reverse('prestamos_list'))

    def get(self, request, *args, **kwargs):
        prestamos = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(instance=prestamos)
        pre_prod = Pre_prod.objects.filter(id_prestamo=prestamos)
        return render(request, self.template_name, {'form': form, 'pre_prod': pre_prod})


class PrestamosDelete(DeleteView):
    model = Prestamo
    success_url = reverse_lazy('prestamos_list')
    template_name = 'salidas/prestamos_delete.html'


def PrestamoBuscar(request):
    buscarprestamo = Prestamo.objects.filter(estado=request.POST['estado'])
    context = {'object_list': buscarprestamo}
    return render(request, 'salidas/prestamos_list.html', context)


def ProductoViewAjax(request, pk):
    producto = Producto.objects.get(id_prod=pk)
    return render(request, 'salidas/bloqueProducto.html', {'producto': producto})


def ProductoListAjax(request):
    productos = Producto.objects.all().extra(select={'id': 'id_prod', 'text': 'nombre'}).values('id', 'text')
    productos_list = list(productos)
    return JsonResponse(productos_list, safe=False)