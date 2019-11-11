from django import forms
from django.http import HttpResponseRedirect



from .models import Proveedor, Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto

        exclude = ['cod_barra', 'merma', 'estado_prod', 'estado', 'precio_venta', 'stock', 'id_cat', 'stock_min']

        labels = {
            'nombre' : 'Nombre producto',
            'descripcion' : 'Descripcion',
            'precio_compra' : 'Precio compra',
            'codigo' : 'Codigo Producto'
        }

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_compra' : forms.NumberInput(attrs={'class':'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor

        exclude = ['estado']

        labels = {
            'rut' : 'Rut',
            'nombre' : 'Nombre',
            'direccion' : 'Direccion',
            'telefono' : 'Telefono',
            'email' : 'Email',
            #'estado' : 'estado',
            'nom_cont' : 'Nombre Contacto',
        }

        widgets = {
            'rut' : forms.TextInput(attrs={'class':'form-control rut','placeholder':'123456789-k'}),
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
            'nom_cont' : forms.TextInput(attrs={'class':'form-control'}),
        }



