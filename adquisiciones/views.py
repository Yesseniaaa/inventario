from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, DetailView

from inventario.models import Categoria
from .form import IngresoForm, ProveedorForm, OrdenAdqForm, ProductoForm, OrdenAdqInfo, OrdenAdqReturnForm, \
    DevolucionForm
from .models import Proveedor, OrdenAdq, Ingreso, Producto, RegistroTemporalProducto, Devolucion


@login_required()
def index(request):
    return render(request, 'adquisiciones/index.html')


class ProductoCreate(CreateView, LoginRequiredMixin):
    model = Producto
    form_class = ProductoForm
    template_name = 'adquisiciones/producto_form.html'
    success_url = reverse_lazy('adquisiciones_producto')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            producto = Producto.objects.filter(nombre=request.POST.get('nombre'))
            cat = Categoria.objects.get(id=request.POST.get('id_cat'))


            p = Producto(nombre=request.POST.get('nombre'), descripcion=request.POST.get('descripcion'),
                         precio_compra=request.POST.get('precio_compra'), stock=request.POST.get('stock'))
            if producto.count() > 0:
                return render(request, self.template_name, {'form': form, 'mensaje': 'errorUnique'})
            p.save()
            p.id_cat.add(cat)
            form = self.form_class
            return render(request, self.template_name, {'form': form, 'mensaje': 'success'})
        except:
            return render(request, self.template_name, {'form': form})
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


@login_required()
def ProductoCreateAjax(request):
    form = ProductoForm(request.POST)
    producto = Producto.objects.filter(nombre=request.POST.get('nombre'))
    p = Producto(nombre=request.POST.get('nombre'), descripcion=request.POST.get('descripcion'),
                 precio_compra=request.POST.get('precio_compra'), stock_min=0)
    cat = Categoria.objects.get(id=request.POST.get('id_cat'))
    try:
        if producto.count() > 0:
            return JsonResponse({'mensaje': 'errorUnique'}, safe=False)
        p.save()
        p.id_cat.add(cat)
        producto = p
        return JsonResponse({'mensaje': 'success', 'id_producto': producto.id_prod, 'texto_producto': producto.nombre},
                            safe=False)
    except:
        return JsonResponse({'mensaje': 'errorInvalido', 'errores': form.errors}, safe=False)


class ProveedorList(ListView, LoginRequiredMixin):
    model = Proveedor
    template_name = 'adquisiciones/proveedor_list.html'


class DevolucionList(ListView, LoginRequiredMixin):
    queryset = Devolucion.objects.select_related('id_producto').all()
    template_name = 'adquisiciones/devolucion_list.html'


class SelectView(View, LoginRequiredMixin):
    template_name = 'adquisiciones/ord_adq_create.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)


class ProveedorCreate(CreateView, LoginRequiredMixin):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'adquisiciones/proveedor_form.html'
    success_url = reverse_lazy('adquisiciones_proveedores')


class ProveedorUpdate(UpdateView, LoginRequiredMixin):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'adquisiciones/proveedor_form.html'
    success_url = reverse_lazy('adquisiciones_proveedores')


class ProveedorDelete(DeleteView, LoginRequiredMixin):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'adquisiciones/proveedor_delete.html'
    success_url = reverse_lazy('adquisiciones_proveedores')


class ProveedorSoftDelete(View, LoginRequiredMixin):
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


class ProveedorActivar(View, LoginRequiredMixin):
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


@login_required()
def OrdenAdqList(request):
    ordAdq = OrdenAdq.objects.all()
    productos = Producto.objects.all()
    context = {'ordAdq': ordAdq, 'productos': productos}
    for producto in productos:
        if producto.stock < producto.stock_min and producto.estado_prod is True:
            messages.warning(request, "Aviso: Hay productos que están con bajo stock. Revisar inventario.")
            return render(request, 'adquisiciones/ord_adq_list.html', context)
    return render(request, 'adquisiciones/ord_adq_list.html', context)


class OrdenAdqCreate(CreateView, LoginRequiredMixin):
    model = OrdenAdq
    form_class = OrdenAdqForm
    categorias = Categoria.objects.all()
    # template_name = 'adquisiciones/ord_adq_form.html'
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
                if (productos_value_precio[count] != '' and productos_value_precio[count] != 0) or (
                        productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                    Ingreso.objects.create(id_adq_id=adquisicion.id, id_prod_id=producto,
                                           precio_compra=productos_value_precio[count],
                                           cantidad=productos_value_cantidad[count])
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        categoriasArray = []
        for categoria in self.categorias:
            categoriasArray.append({'id': categoria.id, 'text': categoria.nombre})
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'categorias': categoriasArray})


class OrdenAdqCreateInvoce(CreateView, LoginRequiredMixin):
    model = OrdenAdq
    form_class = OrdenAdqForm
    categorias = Categoria.objects.all()
    template_name = 'adquisiciones/ord_adq_form.html'
    # template_name = 'adquisiciones/ord_adq_create.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            adquisicion = form.save()
            productos_id = request.POST.getlist('productos_ids')
            productos_value_precio = request.POST.getlist('productos_precio')
            productos_value_cantidad = request.POST.getlist('productos_cantidad')
            for count, productoStr in enumerate(productos_id, start=0):
                producto = int(productoStr)
                if (productos_value_precio[count] != '' and productos_value_precio[count] != 0) or (
                        productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                    Ingreso.objects.create(id_adq_id=adquisicion.id, id_prod_id=producto,
                                           precio_compra=productos_value_precio[count],
                                           cantidad=productos_value_cantidad[count])
                    p = Producto.objects.get(pk=producto)
                    p.stock = F('stock') + productos_value_cantidad[count]
                    ultimo_historial = RegistroTemporalProducto.objects.filter(id_prod_id=producto).order_by('created')
                    if ultimo_historial.__len__() < 1:
                        hist = RegistroTemporalProducto(id_prod=p, stock=productos_value_cantidad[count],
                                                        precio_compra=productos_value_precio[count])
                    else:
                        ultimo_stock = ultimo_historial.last().stock
                        ultimo_precio = ultimo_historial.last().precio_compra
                        nuevo_stock = int(productos_value_cantidad[count]) + ultimo_stock
                        nuevo_precio = (ultimo_precio * ultimo_stock + int(productos_value_cantidad[count]) *
                                        float(productos_value_precio[count])) / nuevo_stock
                        hist = RegistroTemporalProducto(id_prod=p, stock=int(productos_value_cantidad[count]),
                                                        precio_compra=nuevo_precio)
                    hist.save()
                    p.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        categoriasArray = []
        for categoria in self.categorias:
            categoriasArray.append({'id': categoria.id, 'text': categoria.nombre})
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'categorias': categoriasArray})


class OrdenAdqCreateReturn(CreateView, LoginRequiredMixin):
    model = Producto
    form_class = OrdenAdqReturnForm
    template_name = 'adquisiciones/ord_adq_form_return.html'
    success_url = reverse_lazy('adquisiciones_ordenes_devoluciones')

    def post(self, request, *args, **kwargs):
        dev = Devolucion(cantidad=request.POST.get('cantidad'), fecha=request.POST.get('fecha'),
                         id_producto_id=request.POST.get('producto_id'))
        dev.save()
        p = Producto.objects.get(pk=request.POST.get('producto_id'))
        p.stock = F('stock') + request.POST.get('cantidad')
        p.save()
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class OrdenAdqInfo(UpdateView, LoginRequiredMixin):
    model = OrdenAdq
    form_class = OrdenAdqInfo
    template_name = 'adquisiciones/ord_adq_info.html'
    success_url = reverse_lazy('adquisiciones_ordenes_adquisiciones')

    def get(self, request, *args, **kwargs):
        orden_adquisicion = self.model.objects.get(id=kwargs['pk'])
        proveedor = Proveedor.objects.get(id=orden_adquisicion.id_prov_id)
        producto = Producto.objects.get(id_prod=orden_adquisicion.id_prov_id)
        ingresos = Ingreso.objects.filter(id_adq_id=kwargs['pk'])
        form = self.form_class()
        return render(request, self.template_name,
                      {'orden_adquisicion': orden_adquisicion, 'productos': ingresos, 'proveedor': proveedor})


class OrdenAdqUpdate(UpdateView, LoginRequiredMixin):
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
                if (productos_value_precio[count] != '' and productos_value_precio[count] != 0) or (
                        productos_value_cantidad[count] != '' and productos_value_cantidad[count] != 0):
                    ingreso = Ingreso.objects.filter(id_adq_id=adquisicion.id).filter(id_prod_id=producto)
                    if ingreso:
                        ingreso.update(precio_compra=productos_value_precio[count],
                                       cantidad=productos_value_cantidad[count])
                    else:
                        Ingreso.objects.create(id_adq_id=adquisicion.id, id_prod_id=producto,
                                               precio_compra=productos_value_precio[count],
                                               cantidad=productos_value_cantidad[count])
        return redirect(reverse('adquisiciones_ordenes_adquisiciones'))

    def get(self, request, *args, **kwargs):
        orden_adquisicion = self.model.objects.get(id=kwargs['pk'])
        form = self.form_class(instance=orden_adquisicion)
        ingresos = Ingreso.objects.filter(id_adq=orden_adquisicion)
        return render(request, self.template_name, {'form': form, 'ingresos': ingresos})


class OrdenAdqState(View, LoginRequiredMixin):
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


class IngresoList(ListView, LoginRequiredMixin):
    model = Ingreso
    template_name = 'adquisiciones/ingreso_list.html'


class IngresoCreate(CreateView, LoginRequiredMixin):
    model = Producto
    form_class = ProductoForm
    template_name = 'adquisiciones/producto_form.html'
    success_url = reverse_lazy('adquisiciones_ingresos')


class IngresoUpdate(UpdateView, LoginRequiredMixin):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'adquisiciones/ingreso_form.html'
    success_url = reverse_lazy('adquisiciones_ingresos')


class IngresoDelete(DeleteView, LoginRequiredMixin):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'adquisiciones/ingreso_delete.html'
    success_url = reverse_lazy('adquisiciones_ingresos')


@login_required()
def ProductoViewAjax(request, pk):
    producto = Producto.objects.get(id_prod=pk)
    return render(request, 'adquisiciones/bloqueProducto.html', {'producto': producto})


@login_required()
def ProductoListAjax(request):
    productos = Producto.objects.all().extra(select={'id': 'id_prod', 'text': 'nombre', 'cod': 'cod_barra'}).values(
        'id', 'text', 'cod')
    productos_list = list(productos)
    return JsonResponse(productos_list, safe=False)


class DetalleDevolucion(LoginRequiredMixin, DetailView):
    model = Devolucion
    template_name = 'adquisiciones/devolucion_info.html'


class EditarDevolucion(LoginRequiredMixin, UpdateView):
    model = Devolucion
    form_class = DevolucionForm
    template_name = 'adquisiciones/devolucion_form.html'
    success_url = reverse_lazy('adquisiciones_ordenes_devoluciones')
