from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages

from .models import Proveedor, Producto, RegistroTemporalProducto
from .form import  ProveedorForm, ProductoForm

def index(request):
    return render(request,'proveedor/index.html')

class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'proveedor/producto_form.html'
    success_url = reverse_lazy('adquisiciones_producto')
    def post(self, request, *args, **kwargs):
            form = self.form_class(request.POST)
            producto = Producto.objects.filter(nombre = request.POST.get('nombre'))
            if form.is_valid():
                if producto.count() > 0:
                    return render(request, self.template_name, {'form':form, 'mensaje': 'errorUnique'})
                form.save()
                form = self.form_class
                return render(request, self.template_name, {'form':form, 'mensaje': 'success'})
            return HttpResponseRedirect(self.success_url)

def ProductoCreateAjax(request):
    form = ProductoForm(request.POST)    
    producto = Producto.objects.filter(nombre = request.POST.get('nombre'))
    if form.is_valid():
        if producto.count() > 0:
            return JsonResponse({'mensaje': 'errorUnique'}, safe=False)
        producto = form.save()
        return JsonResponse({'mensaje': 'success', 'id_producto': producto.id_prod, 'texto_producto': producto.nombre}, safe=False)
    return JsonResponse({'mensaje': 'errorInvalido', 'errores': form.errors}, safe=False)
            
class ProveedorList(ListView):
    model = Proveedor
    template_name = 'proveedor/proveedor_list.html'
    #def get_queryset(self):
        #return Proveedor.objects.filter(estado=True)

class ProveedorCreate(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor_form.html'
    success_url = reverse_lazy('listar_proveedor')


class ProveedorUpdate(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor_form.html'
    success_url = reverse_lazy('listar_proveedor')

class ProveedorDelete(DeleteView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor_delete.html'
    success_url = reverse_lazy('listar_proveedor')

class ProveedorSoftDelete(View):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor_soft_delete.html'
    success_url = reverse_lazy('listar_proveedor')
    def post(self, request, *args, **kwargs):
        proveedor = self.model.objects.get(id=kwargs['pk'])
        proveedor.estado = False
        proveedor.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'id': kwargs['pk']})

class ProveedorActivar(View):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/proveedor_activar.html'
    success_url = reverse_lazy('listar_proveedor')
    def post(self, request, *args, **kwargs):
        proveedor = self.model.objects.get(id=kwargs['pk'])
        proveedor.estado = True
        proveedor.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'id': kwargs['pk']})


def ProductoViewAjax(request, pk):
    producto = Producto.objects.get(id_prod = pk)
    return render(request, 'proveedor/bloqueProducto.html', {'producto': producto})    

def ProductoListAjax(request):
    productos = Producto.objects.all().extra(select={'id':'id_prod', 'text':'nombre'}).values('id', 'text')
    productos_list = list(productos)
    return JsonResponse(productos_list, safe=False)

