from django import forms
from django.http import HttpResponseRedirect



from .models import Ingreso, Proveedor, OrdenAdq, Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto

        exclude = ['cod_barra', 'merma', 'estado_prod', 'estado', 'stock', 'id_cat', 'stock_min']

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




class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso

        fields = {
            'id_prod',
            'id_adq',
            'precio_compra'
        }

        labels = {
            'id_adq' : 'Adquisicion',
            'id_prod' : 'Producto',
            'precio_compra': 'Precio de Compra'

        }

        widgets = {
            'id_adq' : forms.Select(attrs={'class':'form-control'}),
            'id_prod' : forms.Select(attrs={'class':'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'class':'form-control'})

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


class OrdenAdqForm(forms.ModelForm):

    id_prov = forms.ModelChoiceField(label='Proveedor', queryset=Proveedor.objects.all().filter(estado=True).distinct(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = OrdenAdq


        exclude = ['estado','productos','codigo']


            
        labels = {
            'productos' : 'Productos',
            'precio_compra' : 'Precio Compra',
            'cantidad' : 'Cantidad',
            'estado' : 'Estado'
        }

        widgets = {
            'productos' : forms.CheckboxSelectMultiple(),
            'precio_compra' : forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly', 'value':'0' , 'id':'totalPrecio'}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly', 'value':'0' , 'id':'totalCantidad'}),
            'estado': forms.Select(attrs={'class':'form-control'})

        }


class OrdenAdqInfo(forms.ModelForm):
    class Meta:
        model = OrdenAdq
        form_class = OrdenAdqForm

        exclude = ['productos']

        fields = '__all__'

        id_prov = forms.CharField(disabled=True)
        productos = forms.CharField(disabled=True)
        precio_compra = forms.CharField(disabled=True)
        cantidad = forms.CharField(disabled=True)
        estado = forms.CharField(disabled=True)
        codigo = forms.CharField(disabled=True)


        labels = {
            'id_prov' : 'Proveedor',
            'productos' : 'Productos',
            'precio_compra' : 'Precio Compra',
            'cantidad' : 'Cantidad',
            'estado' : 'Estado',
            'codigo' : 'Codigo adquisicion'
        }

        widgets = {
            'id_prov' : forms.Select(attrs={'class':'form-control', 'readonly':'readonly'}),
            'productos' : forms.CheckboxSelectMultiple(attrs={'readonly':'readonly'}),
            'precio_compra' : forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'cantidad': forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'estado': forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'})

        }


class OrdenAdqFormState(forms.ModelForm):
    class Meta:
        model = OrdenAdq
        form_class = OrdenAdqForm

        exclude = ['id_prov','productos','precio_compra','cantidad']

        labels = {
            'estado' : 'Estado'
        }

        widgets = {

            'estado': forms.Select(attrs={'class':'form-control'})

        }

