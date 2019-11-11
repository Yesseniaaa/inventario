from django import forms
from django.http import HttpResponseRedirect



from .models import Ingreso, Usuario, Prestamo, Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto

        exclude = ['cod_barra', 'merma', 'estado_prod', 'estado', 'stock', 'id_cat', 'stock_min']

        labels = {
            'nombre' : 'Nombre producto',
            'descripcion' : 'Descripcion',
            'codigo' : 'Codigo Producto'
        }

        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        }




class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso

        fields = {
            'id_prod',
            'id_pres',
        }

        labels = {
            'id_prod' : 'Producto',
            'id_pres' : 'Prestamo',
        }

        widgets = {
            'id_prod' : forms.Select(attrs={'class':'form-control'}),
            'id_pres' : forms.Select(attrs={'class':'form-control'}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        exclude = ['estado']

        labels = {
            'rut' : 'Rut',
            'nombre' : 'Nombre',
            'direccion' : 'Direccion',
            'telefono' : 'Telefono',
            'email' : 'Email',
            #'estado' : 'estado',
        }

        widgets = {
            'rut' : forms.TextInput(attrs={'class':'form-control rut','placeholder':'123456789-k'}),
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control'}),
            'telefono' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'}),
        }


class PrestamoForm(forms.ModelForm):

    id_user = forms.ModelChoiceField(label='Usuario', queryset=Usuario.objects.all().filter(estado=True).distinct(), widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Prestamo


        exclude = ['estado','productos','codigo']


            
        labels = {
            'productos' : 'Productos',
            'cantidad' : 'Cantidad',
            'estado' : 'Estado'
        }

        widgets = {
            'productos' : forms.CheckboxSelectMultiple(),
            'cantidad': forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly', 'value':'0' , 'id':'totalCantidad'}),
            'estado': forms.Select(attrs={'class':'form-control'})

        }


class PrestamoInfo(forms.ModelForm):
    class Meta:
        model = Prestamo
        form_class = PrestamoForm

        exclude = ['productos']

        fields = '__all__'

        id_user = forms.CharField(disabled=True)
        productos = forms.CharField(disabled=True)
        cantidad = forms.CharField(disabled=True)
        estado = forms.CharField(disabled=True)
        codigo = forms.CharField(disabled=True)


        labels = {
            'id_user' : 'Usuario',
            'productos' : 'Productos',
            'cantidad' : 'Cantidad',
            'estado' : 'Estado',
            'codigo' : 'Codigo prestamo'
        }

        widgets = {
            'id_user' : forms.Select(attrs={'class':'form-control', 'readonly':'readonly'}),
            'productos' : forms.CheckboxSelectMultiple(attrs={'readonly':'readonly'}),
            'cantidad': forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'estado': forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'})

        }


class PrestamoFormState(forms.ModelForm):
    class Meta:
        model = Prestamo
        form_class = PrestamoForm

        exclude = ['id_user','productos','cantidad']

        labels = {
            'estado' : 'Estado'
        }

        widgets = {

            'estado': forms.Select(attrs={'class':'form-control'})

        }

