from openpyxl import Workbook
from django.db.models import CharField, F, Sum, Value

from inventario.models import Producto
from adquisiciones.models import Ingreso
from salidas.models import Recinto, Sal_prod, Salida
from openpyxl.writer.excel import save_virtual_workbook


def generar_virtual_reporte1(producto_id=1, fecha_inicio="2015-01-01", fecha_final="2020-03-23"):
    workbook = Workbook()
    sheet = workbook.active

    producto = Producto.objects.filter(id_prod=producto_id)

    sheet.append([""])
    sheet.append(["Producto: ", producto[0].nombre])
    sheet.append([""])
    sheet.append(["Desde: ", fecha_inicio, "", "Hasta: ", fecha_final])
    sheet.append([""])

    sheet.append(
        ["Fecha", "Descripcion", "Entrada(cantidad)", "Salida(cantidad", "Saldo(cantidad)"]
    )

    entradas = (
        Ingreso.objects.filter(id_prod=producto_id)
        .filter(created__lte=fecha_final)
        .filter(created__gte=fecha_inicio)
        .annotate(
            price=F("precio_compra"),
            entrada=F("cantidad"),
            salida=Value("-", CharField()),
            descripcion=Value("Entrada", CharField()),
        )
        .values_list("updated", "descripcion", "entrada", "salida")
    )
    salidas = (
        Sal_prod.objects.filter(id_prod=producto_id)
        .filter(created__lte=fecha_final)
        .filter(created__gte=fecha_inicio)
        .annotate(
            price=F("precio"),
            entrada=Value("-", CharField()),
            salida=F("cantidad"),
            descripcion=Value("Salida", CharField()),
        )
        .values_list("updated", "descripcion", "entrada", "salida")
    )

    final_qs = entradas.union(salidas).order_by("updated")

    stock_counter = 0

    for res in final_qs:
        stock_counter = stock_counter + res[2] if res[1] == "Entrada" else stock_counter - res[3]
        data = [res[0], res[1], res[2], res[3], stock_counter]
        sheet.append(data)

    return save_virtual_workbook(workbook)


def generar_virtual_reporte2(recinto_id=1, fecha_inicio="2015-01-01", fecha_final="2020-04-23"):
    workbook = Workbook()
    sheet = workbook.active

    recinto = Recinto.objects.filter(id=recinto_id)

    sheet.append([""])
    sheet.append(["Recinto: ", recinto[0].nombre])
    sheet.append([""])
    sheet.append(["Desde: ", fecha_inicio, "", "Hasta: ", fecha_final])
    sheet.append([""])

    sheet.append(["Producto", "Cantidad", "Precio", "Total"])

    salidas = Salida.objects.filter(id_recinto=recinto_id).values("id")
    salida_productos = Sal_prod.objects.filter(id_salida__in=salidas)

    productos = salida_productos.values("id_prod__nombre").annotate(
        precioTotal=Sum("precio"), cantidadTotal=Sum("cantidad"),
    )
    print(productos)

    for producto in productos:
        data = [
            producto["id_prod__nombre"],
            producto["cantidadTotal"],
            producto["precioTotal"],
            producto["cantidadTotal"] * producto["precioTotal"],
        ]
        sheet.append(data)

    return save_virtual_workbook(workbook)
