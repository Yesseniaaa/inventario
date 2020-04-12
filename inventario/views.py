from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from generador_excel.generador import generar_virtual_reporte1, generar_virtual_reporte2
from .forms import *

today = date.today()  # fecha actual


@login_required()
def index(request):
    return render(request, "inventario/index.html")


# Clase Categoria


class CrearCategoria(SuccessMessageMixin, CreateView, LoginRequiredMixin):
    model = Categoria
    form_class = CategoriaForm
    template_name = "inventario/crear_categoria.html"
    success_url = reverse_lazy("crear_categoria")
    success_message = "La categoria fue creada con éxito."


class ListarCategoria(ListView, LoginRequiredMixin):
    model = Categoria
    template_name = "inventario/listar_categoria.html"


@login_required()
def EditarCategoria(request, pk):
    categoria = Categoria.objects.get(id=pk)
    if request.method == "GET":
        form = CategoriaForm(instance=categoria)
    else:
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Se ha actualizado correctamente la categría " + categoria.nombre + "."
            )
        return redirect("listar_categoria")
    return render(
        request, "inventario/editar_categoria.html", {"form": form, "categoria": categoria}
    )


@login_required()
def CategoriaActivar(request, pk):
    categoria = Categoria.objects.get(id=pk)
    categoria.estado = True
    categoria.save()
    return redirect("listar_categoria")


@login_required()
def CategoriaDesactivar(request, pk):
    categoria = Categoria.objects.get(id=pk)
    categoria.estado = False
    categoria.save()
    return redirect("listar_categoria")


# Clase Producto


class ListarProducto(ListView, LoginRequiredMixin):
    model = Producto
    template_name = "inventario/listar_producto.html"


class ListarMerma(ListView, LoginRequiredMixin):
    queryset = MermaM.objects.all().select_related('id_producto')
    template_name = "inventario/listar_merma.html"


@login_required()
def ListarCatProd(request, pk):
    productos = Producto.objects.filter(id_cat=pk)
    # categoria = Categoria.objects.get(id_cat=pk)
    context = {"productos": productos}
    return render(request, "inventario/listar_cat_prod.html", context)


class EditarProducto(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    model = Producto
    form_class = ProductoFormUpdate
    template_name = "inventario/editar_producto.html"
    success_message = "El producto ha sido actualizado con éxito."
    pk = None

    def form_valid(self, form):
        producto = form.save()
        self.pk = producto.pk
        return super(EditarProducto, self).form_valid(form)

    def get_success_url(self):
        return reverse("mostrar_producto", kwargs={"pk": self.pk})


class MostrarProducto(DetailView, LoginRequiredMixin):
    model = Producto
    template_name = "inventario/mostrar_producto.html"


@login_required()
def HistorialPrecio(request, pk):
    precios = RegistroTemporalProducto.objects.filter(id_prod=pk)
    producto = Producto.objects.get(id_prod=pk)
    context = {"precios": precios, "producto": producto}
    return render(request, "inventario/historial_precio.html", context)


@login_required()
def EditarStock(request):
    productos = Producto.objects.all()
    if request.GET.get("cantidad") is not None:
        for producto in productos:
            if request.GET.get("codigo") == producto.cod_barra and producto.estado_prod is False:
                messages.error(
                    request, "El producto " + producto.nombre + " se encuentra deshabilitado."
                )
                return redirect("editar_stock")
            elif request.GET.get("codigo") == producto.cod_barra:
                producto.stock = producto.stock + int(request.GET.get("cantidad"))
                producto.save()
                messages.success(
                    request, "El stock de " + producto.nombre + " ha sido ingresado correctamente."
                )
                return redirect("editar_stock")
        messages.error(request, "El código ingresado no está asociado a ningún producto.")
    return render(request, "inventario/editar_stock.html")


class EditarMerma(CreateView, LoginRequiredMixin):
    model = MermaM
    form_class = MermaForm
    template_name = "inventario/editar_merma.html"
    success_url = reverse_lazy('editar_merma')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        producto = Producto.objects.get(pk=request.POST['id_producto'])
        if producto.stock - int(request.POST['cantidad']) >= 0:
            if form.is_valid():
                form.save()
                producto.merma = F('merma') + int(request.POST['cantidad'])
                producto.stock = F('stock') - int(request.POST['cantidad'])
                producto.save()
                return HttpResponseRedirect(self.success_url)
        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


@login_required()
def ResetearMerma(request, pk):
    producto = Producto.objects.get(id_prod=pk)
    producto.merma = 0
    producto.save()
    messages.success(request, "La merma ha sido reseteada con éxito.")
    return redirect("mostrar_producto", pk=producto.pk)


@login_required()
def ProductoActivar(request, pk):
    producto = Producto.objects.get(id_prod=pk)
    producto.estado_prod = True
    producto.save()
    return redirect("listar_producto")


@login_required()
def ProductoDesactivar(request, pk):
    producto = Producto.objects.get(id_prod=pk)
    producto.estado_prod = False
    producto.save()
    return redirect("listar_producto")


# Estadistica

@login_required()
def MostrarEstadistica(request):
    if request.POST:
        reporte1 = generar_virtual_reporte1(
            producto_id=request.POST["producto_id"],
            fecha_inicio=request.POST["fecha_inicio"],
            fecha_final=request.POST["fecha_fin"],
        )
        response = HttpResponse(
            reporte1,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=Tarjeta de Existencias.xlsx"
        return response
    else:
        form = Reporte1Form()
    return render(request, "inventario/estadistica.html", {"form": form})


@login_required()
def MostrarEstadistica2(request):
    if request.POST:
        try:
            reporte2 = generar_virtual_reporte2(
                recinto_id=request.POST["recinto_id"],
                fecha_inicio=request.POST["fecha_inicio"],
                fecha_final=request.POST["fecha_fin"],
            )
            response = HttpResponse(
                reporte2,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "attachment; filename=Consumo.xlsx"
            return response
        except:
            form = Reporte2Form()
    else:
        form = Reporte2Form()
    return render(request, "inventario/estadistica2.html", {"form": form})


@login_required()
def GetHistorialProducto(request, pk):
    historial = RegistroTemporalProducto.objects.filter(id_prod=pk).values('precio_compra', 'id_prod')
    historial_list = list(historial)
    return JsonResponse(historial_list, safe=False)
