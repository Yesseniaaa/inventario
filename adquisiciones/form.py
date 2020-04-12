from django import forms

from inventario.models import Categoria
from .models import Ingreso, Proveedor, OrdenAdq, Producto, Devolucion


class ProductoForm(forms.ModelForm):
    id_cat = forms.ModelMultipleChoiceField(label="Categoria",
                                            queryset=Categoria.objects.all().filter(estado=True).distinct().order_by(
                                                'nombre'), widget=forms.Select())

    class Meta:
        model = Producto

        exclude = ['merma', 'estado_prod', 'estado', 'stock_min']
        fields = [
            'nombre',
            'cod_barra',
            'descripcion',
            'stock',
            'id_cat',
        ]
        labels = {
            'nombre': 'Nombre producto',
            'cod_barra': 'Codigo',
            'descripcion': 'Descripcion',
            'stock': 'Stock',
            'id_cat': 'Categoria',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_barra': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso

        fields = {
            'id_prod',
            'id_adq',
            'precio_compra'
        }

        labels = {
            'id_adq': 'Adquisicion',
            'id_prod': 'Producto',
            'precio_compra': 'Precio de Compra'

        }

        widgets = {
            'id_adq': forms.Select(attrs={'class': 'form-control'}),
            'id_prod': forms.Select(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'})

        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor

        exclude = ['estado']

        labels = {
            'rut': 'Rut',
            'nombre': 'Nombre',
            'direccion': 'Direccion',
            'telefono': 'Telefono',
            'email': 'Email',
            # 'estado' : 'estado',
            'nom_cont': 'Nombre Contacto',
        }

        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control rut', 'placeholder': '123456789-k'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nom_cont': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrdenAdqReturnForm(forms.ModelForm):
    producto_id = forms.ModelChoiceField(
        queryset=Producto.objects.all(), empty_label=None, label="Productos"
    )

    fecha = forms.DateField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"),
    )

    precio_calc = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '0', 'id': 'precioCalc'})
    )

    class Meta:
        model = Devolucion

        fields = ['producto_id', 'fecha', 'cantidad']


class OrdenAdqForm(forms.ModelForm):
    id_prov = forms.ModelChoiceField(label='Proveedor', queryset=Proveedor.objects.all().filter(estado=True).distinct(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = OrdenAdq

        exclude = ['estado', 'productos', 'codigo']

        labels = {
            'factura': 'Numero de factura',
            'fecha_factura': 'Fecha factura',
            'productos': 'Productos',
            'precio_compra': 'Precio Compra',
            'cantidad': 'Cantidad',
            'estado': 'Estado'
        }

        widgets = {
            'factura': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_factura': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'productos': forms.CheckboxSelectMultiple(),
            'precio_compra': forms.NumberInput(
                attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '0', 'id': 'totalPrecio'}),
            'cantidad': forms.NumberInput(
                attrs={'class': 'form-control', 'readonly': 'readonly', 'value': '0', 'id': 'totalCantidad'}),
            'estado': forms.Select(attrs={'class': 'form-control'})

        }


class OrdenAdqInfo(forms.ModelForm):
    class Meta:
        model = OrdenAdq
        form_class = OrdenAdqForm

        exclude = ['productos']

        fields = '__all__'

        id_prov = forms.CharField(disabled=True)
        factura = forms.CharField(disabled=True)
        fecha_factura = forms.CharField(disabled=True)
        productos = forms.CharField(disabled=True)
        precio_compra = forms.CharField(disabled=True)
        cantidad = forms.CharField(disabled=True)
        estado = forms.CharField(disabled=True)
        codigo = forms.CharField(disabled=True)

        labels = {
            'id_prov': 'Proveedor',
            'factura': 'Numero de factura',
            'fecha_factura': 'Fecha factura',
            'productos': 'Productos',
            'precio_compra': 'Precio Compra',
            'cantidad': 'Cantidad',
            'estado': 'Estado',
            'codigo': 'Codigo adquisicion'
        }

        widgets = {
            'id_prov': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'factura': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'fecha_factura': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'},
                                             format="%Y-%m-%d"),
            'productos': forms.CheckboxSelectMultiple(attrs={'readonly': 'readonly'}),
            'precio_compra': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})

        }


class OrdenAdqFormState(forms.ModelForm):
    class Meta:
        model = OrdenAdq
        form_class = OrdenAdqForm

        exclude = ['id_prov', 'productos', 'precio_compra', 'cantidad']

        labels = {
            'estado': 'Estado'
        }

        widgets = {

            'estado': forms.Select(attrs={'class': 'form-control'})

        }

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Devolucion

        fields = ['id_producto', 'fecha', 'cantidad']

