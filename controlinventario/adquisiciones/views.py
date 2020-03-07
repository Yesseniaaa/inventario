from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages

from .models import Proveedor, OrdenAdq, Ingreso, Producto, RegistroTemporalProducto
from .form import IngresoForm, ProveedorForm, OrdenAdqForm, ProductoForm, OrdenAdqInfo, OrdenAdqReturnForm

def index(request):
    return render(request,'adquisiciones/index.html')

class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'adquisiciones/producto_form.html'
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
    template_name = 'adquisiciones/proveedor_list.html'

class ProveedorCreate(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'adquisiciones/proveedor_form.html'
    success_url = reverse_lazy('adquisiciones_proveedores')


class ProveedorUpdate(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'adquisiciones/proveedor_form.html'
    success_url = reverse_lazy('adquisiciones_proveedores')

class ProveedorDelete(DeleteView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'adquisiciones/proveedor_delete.html'
    success_url = reverse_lazy('adquisiciones_proveedores')

class ProveedorSoftDelete(View):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'adquisiciones/proveedor_soft_delete.html'
    success_url = reverse_lazy('adquisiciones_proveedores')
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
    template_name = 'adquisiciones/proveedor_activar.html'
    success_url = reverse_lazy('adquisiciones_proveedores')
    def post(self, request, *args, **kwargs):
        proveedor = self.model.objects.get(id=kwargs['pk'])
        proveedor.estado = True
        proveedor.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'id': kwargs['pk']})

def OrdenAdqList(request):
    ordAdq = OrdenAdq.objects.all()
    productos = Producto.objects.all()
    context = {'ordAdq':ordAdq, 'productos':productos}
    for producto in productos:
        if producto.stock < producto.stock_min and producto.estado_prod is True:
            messages.warning(request, "Aviso: Hay productos que están con bajo stock. Revisar inventario.")
            return render(request, 'adquisiciones/ord_adq_list.html', context)
    return render(request, 'adquisiciones/ord_adq_list.html', context)

class OrdenAdqCreate(CreateView):
    model = OrdenAdq
    form_class = OrdenAdqForm
   #template_name = 'adquisiciones/ord_adq_form.html'
    template_name = 'adquisiciones/ord_adq_create.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            adquisicion = form.save()
            productos_id = request.POST.getlist('productos_ids')
            productos_value_precio = request.POST.getlist('productos_precio')
            productos_value_cantidad = request.POST.getlist('productos_cantidad')
            for count, producto in enumerate(productos_id, start=0):
                if (productos_value_precio[count] != '' and productos_value_precio[count] != 0) or (productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                   Ingreso.objects.create(id_adq_id=adquisicion.id, id_prod_id=producto, precio_compra=productos_value_precio[count], cantidad=productos_value_cantidad[count])
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

class OrdenAdqCreateInvoce(CreateView):
    model = OrdenAdq
    form_class = OrdenAdqForm
    template_name = 'adquisiciones/ord_adq_form.html'
    #template_name = 'adquisiciones/ord_adq_create.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            adquisicion = form.save()
            productos_id = request.POST.getlist('productos_ids')
            productos_value_precio = request.POST.getlist('productos_precio')
            productos_value_cantidad = request.POST.getlist('productos_cantidad')
            for count, producto in enumerate(productos_id, start=0):
                if (productos_value_precio[count] != '' and productos_value_precio[count] != 0) or (productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                   Ingreso.objects.create(id_adq_id=adquisicion.id, id_prod_id=producto, precio_compra=productos_value_precio[count], cantidad=productos_value_cantidad[count])
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

class OrdenAdqCreateReturn(CreateView):
    model = Producto
    #form_class = OrdenAdqReturnForm
    template_name = 'adquisiciones/ord_adq_form_return.html'
    #template_name = 'adquisiciones/ord_adq_create.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
       # if form.is_valid():
            #devolucion = form.save()
            code = request.POST.getlist('code')
            productos_value_name = request.POST.getlist('name')
            productos_value_cantidad = request.POST.getlist('productos_cantidad')
            #for count, producto in enumerate(productos_id, start=0):
               # if (productos_value_precio[count] != '' and productos_value_precio[count] != 0) or (productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                #   Ingreso.objects.create(id_adq_id=adquisicion.id, id_prod_id=producto, precio_compra=productos_value_precio[count], cantidad=productos_value_cantidad[count])
            return redirect(self.success_url)
            return render(request, self.template_name) 

    def get(self, request, *args, **kwargs):
        #form = self.form_class()
        print("get OrdenAdqCreateReturn ")
        return render(request, self.template_name)        

class OrdenAdqInfo(UpdateView):
    model = OrdenAdq
    form_class = OrdenAdqInfo
    template_name = 'adquisiciones/ord_adq_info.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def get(self, request, *args, **kwargs):
        orden_adquisicion = self.model.objects.get(id=kwargs['pk'])
        proveedor = Proveedor.objects.get(id = orden_adquisicion.id_prov_id)
        producto = Producto.objects.get(id_prod= orden_adquisicion.id_prov_id)
        ingresos = Ingreso.objects.filter(id_adq_id = kwargs['pk'])
        form = self.form_class()
        return render(request, self.template_name, {'orden_adquisicion':orden_adquisicion, 'productos': ingresos, 'proveedor': proveedor})


class OrdenAdqUpdate(UpdateView):
    model = OrdenAdq
    form_class = OrdenAdqForm
    template_name = 'adquisiciones/ord_adq_form.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        orden_adquisicion = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(request.POST, instance=orden_adquisicion)
        if form.is_valid():
            adquisicion = form.save()

            productos_id = request.POST.getlist('productos_ids')
            productos_value_precio = request.POST.getlist('productos_precio')
            productos_value_cantidad = request.POST.getlist('productos_cantidad')

            for count, producto in enumerate(productos_id, start=0):
                if (productos_value_precio[count] != '' and productos_value_precio[count] != 0) or (productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                    ingreso = Ingreso.objects.filter(id_adq_id=adquisicion.id).filter(id_prod_id=producto)
                    if ingreso:
                        ingreso.update(precio_compra=productos_value_precio[count], cantidad=productos_value_cantidad[count])
                    else:
                        Ingreso.objects.create(id_adq_id=adquisicion.id, id_prod_id=producto, precio_compra=productos_value_precio[count], cantidad=productos_value_cantidad[count])
        return redirect(reverse('adquisiciones_ordenes_adquisiciones'))

    def get(self, request, *args, **kwargs):
        orden_adquisicion = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(instance=orden_adquisicion)
        ingresos = Ingreso.objects.filter(id_adq = orden_adquisicion)
        return render(request, self.template_name, {'form': form , 'ingresos': ingresos})

class OrdenAdqState(View):
    model = OrdenAdq
    form_class = OrdenAdqForm
    template_name = 'adquisiciones/ord_adq_state.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        orden_adq = self.model.objects.get(id=kwargs['pk'])
        orden_adq.estado = 'pagado'
        ingresos = Ingreso.objects.filter(id_adq_id=orden_adq)
        for ingreso in ingresos:
            producto = Producto.objects.get(id_prod=ingreso.id_prod_id)
            producto.stock += ingreso.cantidad
            producto.precio_compra = ingreso.precio_compra
            producto.save()
            registros = RegistroTemporalProducto.objects.filter(id_prod_id=ingreso.id_prod_id).order_by('-id')[:1]
            suma = 0
            totalCantidad = 0
            if registros.count() is None:
                RegistroTemporalProducto.objects.create(id_prod_id=ingreso.id_prod_id,
                                                        precio_compra=ingreso.precio_compra,
                                                        stock=ingreso.cantidad)
            else:
                for registro in registros:
                    totalCantidad = producto.stock
                suma = ingreso.precio_compra * ingreso.cantidad
                totalCantidad += ingreso.cantidad
                resultado = int(suma / totalCantidad)
                RegistroTemporalProducto.objects.create(id_prod_id=ingreso.id_prod_id,
                                                        precio_compra=ingreso.precio_compra,
                                                        stock=ingreso.cantidad)
        orden_adq.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'id': kwargs['pk']})


class IngresoList(ListView):
    model = Ingreso
    template_name = 'adquisiciones/ingreso_list.html'

class IngresoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'adquisiciones/producto_form.html'
    success_url = reverse_lazy('adquisiciones_ingresos')

class IngresoUpdate(UpdateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'adquisiciones/ingreso_form.html'
    success_url = reverse_lazy('adquisiciones_ingresos')

class IngresoDelete(DeleteView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'adquisiciones/ingreso_delete.html'
    success_url = reverse_lazy('adquisiciones_ingresos')

def ProductoViewAjax(request, pk):
    producto = Producto.objects.get(id_prod = pk)
    return render(request, 'adquisiciones/bloqueProducto.html', {'producto': producto})    

def ProductoListAjax(request):
    productos = Producto.objects.all().extra(select={'id':'id_prod', 'text':'nombre', 'cod':'cod_barra'}).values('id', 'text', 'cod')
    productos_list = list(productos)
    return JsonResponse(productos_list, safe=False)