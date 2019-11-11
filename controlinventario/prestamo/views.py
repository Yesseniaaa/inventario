from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages

from .models import Usuario, Prestamo, Ingreso, Producto, RegistroTemporalProducto
from .form import IngresoForm, UsuarioForm, PrestamoForm, ProductoForm, PrestamoInfo

def index(request):
    return render(request,'prestamo/index.html')

# Clase Prestamo

def PrestamoList(request):
    ordAdq = Prestamo.objects.all()
    productos = Producto.objects.all()
    context = {'ordAdq':ordAdq, 'productos':productos}
    for producto in productos:
        if producto.stock < producto.stock_min and producto.estado_prod is True:
            messages.warning(request, "Aviso: Hay productos que están con bajo stock. Revisar inventario.")
            return render(request, 'prestamo/prestamo_list.html', context)
    return render(request, 'prestamo/prestamo_list.html', context)

class PrestamoCreate(CreateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamo/prestamo_form.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            adquisicion = form.save()
            productos_id = request.POST.getlist('productos_ids')
            productos_value_cantidad = request.POST.getlist('productos_cantidad')
            for count, producto in enumerate(productos_id, start=0):
                if (productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                   Ingreso.objects.create(id_pres_id=adquisicion.id, id_prod_id=producto, cantidad=productos_value_cantidad[count])
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

class PrestamoInfo(UpdateView):
    model = Prestamo
    form_class = PrestamoInfo
    template_name = 'prestamo/prestamo_info.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def get(self, request, *args, **kwargs):
        prestamo = self.model.objects.get(id=kwargs['pk'])
        usuario = Usuario.objects.get(id = prestamo.id_user_id)
        producto = Producto.objects.get(id_prod= prestamo.id_user_id)
        ingresos = Ingreso.objects.filter(id_pres_id = kwargs['pk'])
        form = self.form_class()
        return render(request, self.template_name, {'prestamo':prestamo, 'productos': ingresos, 'usuario': usuario})


class PrestamoUpdate(UpdateView):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamo/prestamo_form.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        prestamo = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(request.POST, instance=prestamo)
        if form.is_valid():
            adquisicion = form.save()

            productos_id = request.POST.getlist('productos_ids')
            productos_value_cantidad = request.POST.getlist('productos_cantidad')

            for count, producto in enumerate(productos_id, start=0):
                if (productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                    ingreso = Ingreso.objects.filter(id_pres_id=adquisicion.id).filter(id_prod_id=producto)
                    if ingreso:
                        ingreso.update(cantidad=productos_value_cantidad[count])
                    else:
                        Ingreso.objects.create(id_pres_id=adquisicion.id, id_prod_id=producto, cantidad=productos_value_cantidad[count])
        return redirect(reverse('adquisiciones_ordenes_adquisiciones'))

    def get(self, request, *args, **kwargs):
        prestamo = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(instance=prestamo)
        ingresos = Ingreso.objects.filter(id_pres = prestamo)
        return render(request, self.template_name, {'form': form , 'ingresos': ingresos})

class PrestamoState(View):
    model = Prestamo
    form_class = PrestamoForm
    template_name = 'prestamo/prestamo_state.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        pres = self.model.objects.get(id=kwargs['pk'])
        pres.estado = 'Entregado'
        ingresos = Ingreso.objects.filter(id_pres_id=pres)
        for ingreso in ingresos:
            producto = Producto.objects.get(id_prod=ingreso.id_prod_id)
            #producto.stock += ingreso.cantidad
            producto.save()
            registros = RegistroTemporalProducto.objects.filter(id_prod_id=ingreso.id_prod_id).order_by('-id')[:1]
            suma = 0
            totalCantidad = 0
            if registros.count() is None:
                RegistroTemporalProducto.objects.create(id_prod_id=ingreso.id_prod_id,
                                                        stock=ingreso.cantidad)
            else:
                for registro in registros:
                    totalCantidad = producto.stock
                totalCantidad += ingreso.cantidad
                RegistroTemporalProducto.objects.create(id_prod_id=ingreso.id_prod_id,
                                                        stock=ingreso.cantidad)
        pres.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'id': kwargs['pk']})

# Class Usuario

class UsuarioList(ListView):
    model = Usuario
    template_name = 'prestamo/usuario_list.html'
    #def get_queryset(self):
        #return Usuario.objects.filter(estado=True)

class UsuarioCreate(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'prestamo/usuario_form.html'
    success_url = reverse_lazy('listar_usuario')


class UsuarioUpdate(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'prestamo/usuario_form.html'
    success_url = reverse_lazy('listar_usuario')

class UsuarioDelete(DeleteView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'prestamo/usuario_delete.html'
    success_url = reverse_lazy('listar_usuario')

class UsuarioSoftDelete(View):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'prestamo/usuario_soft_delete.html'
    success_url = reverse_lazy('listar_usuario')
    def post(self, request, *args, **kwargs):
        usuario = self.model.objects.get(id=kwargs['pk'])
        usuario.estado = False
        usuario.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'id': kwargs['pk']})

class UsuarioActivar(View):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'prestamo/usuario_activar.html'
    success_url = reverse_lazy('listar_usuario')
    def post(self, request, *args, **kwargs):
        usuario = self.model.objects.get(id=kwargs['pk'])
        usuario.estado = True
        usuario.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'id': kwargs['pk']})

# Class Ingreso

class IngresoList(ListView):
    model = Ingreso
    template_name = 'prestamo/ingreso_list.html'

class IngresoCreate(CreateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'prestamo/ingreso_form.html'
    success_url = reverse_lazy('adquisiciones_ingresos')

class IngresoUpdate(UpdateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'prestamo/ingreso_form.html'
    success_url = reverse_lazy('adquisiciones_ingresos')

class IngresoDelete(DeleteView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'prestamo/ingreso_delete.html'
    success_url = reverse_lazy('adquisiciones_ingresos')

class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'prestamo/producto_form.html'
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

def ProductoViewAjax(request, pk):
    producto = Producto.objects.get(id_prod = pk)
    return render(request, 'mod_adquisiciones/bloqueProducto.html', {'producto': producto})    

def ProductoListAjax(request):
    productos = Producto.objects.all().extra(select={'id':'id_prod', 'text':'nombre'}).values('id', 'text')
    productos_list = list(productos)
    return JsonResponse(productos_list, safe=False)