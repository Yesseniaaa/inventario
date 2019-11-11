from django.shortcuts import render, redirect, reverse
from .forms import *
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from inventario.models import Producto
from datetime import date
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
today = date.today() #fecha actual

def index(request):
    return render(request,'inventario/index.html')

# Clase Categoria

class CrearCategoria(SuccessMessageMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'inventario/crear_categoria.html'
    success_url = reverse_lazy('crear_categoria')
    success_message = "La categoria fue creada con éxito."

class ListarCategoria(ListView):
    model = Categoria
    template_name = 'inventario/listar_categoria.html'

def EditarCategoria(request,pk):
    categoria = Categoria.objects.get(id=pk)
    if request.method == 'GET':
        form = CategoriaForm(instance=categoria)
    else:
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Se ha actualizado correctamente la categría " + categoria.nombre + ".")
        return redirect('listar_categoria')
    return render(request, 'inventario/editar_categoria.html', {'form':form, 'categoria':categoria})

def CategoriaActivar(request,pk):
    categoria = Categoria.objects.get(id=pk)
    categoria.estado = True
    categoria.save()
    return redirect('listar_categoria')

def CategoriaDesactivar(request,pk):
    categoria = Categoria.objects.get(id=pk)
    categoria.estado = False
    categoria.save()
    return redirect('listar_categoria')

# Clase Producto

class CrearProducto(SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/crear_producto.html'
    success_url = reverse_lazy('crear_producto')
    success_message = "El producto fue creado con éxito."

class ListarProducto(ListView):
    model = Producto
    template_name = 'inventario/listar_producto.html'

class EditarProducto(SuccessMessageMixin,UpdateView):
    model = Producto
    form_class = ProductoFormUpdate
    template_name = 'inventario/editar_producto.html'
    success_message = "El producto ha sido actualizado con éxito."
    pk = None

    def form_valid(self, form):
        producto = form.save()
        self.pk = producto.pk
        return super(EditarProducto, self).form_valid(form)

    def get_success_url(self):
        return reverse('mostrar_producto', kwargs={'pk':self.pk})

class MostrarProducto(DetailView):
    model = Producto
    template_name = 'inventario/mostrar_producto.html'


def EditarStock(request):
    productos = Producto.objects.all()
    if request.GET.get('cantidad') is not None:
        for producto in productos:
            if request.GET.get('codigo') == producto.cod_barra and producto.estado_prod is False:
                messages.error(request, "El producto " + producto.nombre + " se encuentra deshabilitado.")
                return redirect('editar_stock')
            elif request.GET.get('codigo') == producto.cod_barra:
                producto.stock = producto.stock + int(request.GET.get('cantidad'))
                producto.save()
                messages.success(request, "El stock de " + producto.nombre + " ha sido ingresado correctamente.")
                return redirect('editar_stock')
        messages.error(request, "El código ingresado no está asociado a ningún producto.")
    return render(request, 'inventario/editar_stock.html')

def EditarMerma(request):
    productos = Producto.objects.all()
    if request.GET.get('codigo') is not None:
        for producto in productos:
            if request.GET.get('codigo') == producto.cod_barra and producto.estado_prod is False:
                messages.error(request, "El producto " + producto.nombre + " se encuentra deshabilitado.")
                return redirect('editar_merma')
            elif request.GET.get('codigo') == producto.cod_barra:
                producto.merma += int(request.GET.get('merma'))
                producto.stock += -int(request.GET.get('merma'))
                if producto.stock < 0:
                    messages.error(request, "El stock no puede ser menor a cero.")
                    return redirect('editar_merma')
                producto.save()
                messages.success(request, "La merma de " + producto.nombre + " ha sido ingresada correctamente.")
                return redirect('editar_merma')
        messages.error(request, "El código ingresado no está asociado a ningún producto.")
    return render(request, 'inventario/editar_merma.html')

def ResetearMerma(request,pk):
    producto = Producto.objects.get(id_prod=pk)
    producto.merma = 0
    producto.save()
    messages.success(request, "La merma ha sido reseteada con éxito.")
    return redirect('mostrar_producto', pk=producto.pk)

def ProductoActivar(request,pk):
    producto = Producto.objects.get(id_prod=pk)
    producto.estado_prod = True
    producto.save()
    return redirect('listar_producto')

def ProductoDesactivar(request,pk):
    producto = Producto.objects.get(id_prod=pk)
    producto.estado_prod = False
    producto.save()
    return redirect('listar_producto')

# Estadistica

def MostrarEstadistica(request):
    Productos = Producto.objects.all()
    if request.POST:
        idproductoBuscado = request.POST.get('producto')
        producto = Producto.objects.get(id_prod=idproductoBuscado)
        registro_temporal_productos = RegistroTemporalProducto.objects.filter(id_prod_id=idproductoBuscado, created__year=today.year)
        context = {'productos':Productos, 'registro_temporal_productos':registro_temporal_productos, 'productoBuscado':producto}
        return render(request,'inventario/estadistica.html', context)
    context = {'productos':Productos}
    return render(request,'inventario/estadistica.html', context)