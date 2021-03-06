from django import forms
from .models import *

class RecintoForm(forms.ModelForm):
    class Meta:
        model = Recinto
        fields = [
            'nombre',
            'descripcion',
        ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FuncionarioForm(forms.ModelForm):
    id_recinto = forms.ModelMultipleChoiceField(label="Recinto", queryset = Recinto.objects.all().filter(estado = True).distinct().order_by('nombre'), widget = forms.CheckboxSelectMultiple())
    class Meta:
        model = Funcionario
        fields = [
            'rut',
            'nombres',
            'paterno',
            'materno',
            'mail',
            'telefono',
            'cargo',
            'id_recinto',
        ]
        labels = {
            'rut' : 'RUT',
            'nombres' : 'Nombres',
            'paterno' : 'Apellido Paterno',
            'materno' : 'Apellido Materno',
            'mail' : 'Mail',
            'telefono' : 'Teléfono',
            'cargo' : 'Cargo',
            'id_recinto' : 'Recinto',
        }
        widgets = {
            'rut' : forms.TextInput(attrs={'class': 'form-control rut', 'placeholder':'12345678-k'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
			'paterno': forms.TextInput(attrs={'class': 'form-control'}),
			'materno': forms.TextInput(attrs={'class': 'form-control'}),
			'mail': forms.EmailInput(attrs={'class': 'form-control'}),
			'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
			'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'id_recinto': forms.CheckboxSelectMultiple(),
        }
        
class SalidaForm(forms.ModelForm):
    class Meta:
        model = Salida
        exclude = ['productos']
        fields = [
            'id',
            'id_funcionario',
            'id_recinto',
            'total',
            'productos',
        ]

        labels = {

            'id' : 'id entrega',
            'id_funcionario' : 'Funcionario',
            'id_recinto': 'Recinto',
            'total': 'total',
            'productos': 'productos',
        }

        widgets = {
            'id_entrega' : forms.Select(attrs={'class':'form-control'}),
            'id_funcionario' : forms.Select(attrs={'class':'form-control'}),
            'id_recinto' : forms.Select(attrs={'class':'form-control'}),
            'total' : forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly', 'id':'TotalSalida'}),
            'productos' : forms.Select(attrs={'class':'form-control'}),
        }

class Sal_prodForm(forms.ModelForm):
    class Meta:
        model = Sal_prod
        fields = [
            'id_prod',
            'id_salida',
            'precio',
            'cantidad',
        ]

        labels = {

            'id_prod' : 'Productos',
            'id_salida' : 'Salida',
            'precio': 'precio',
            'cantidad': 'cantidad',
        }

        widgets = {
            'id_prod' : forms.Select(attrs={'class':'form-control'}),
            'id_salida' : forms.Select(attrs={'class':'form-control'}),
            'precio' : forms.NumberInput(attrs={'class':'form-control'}),
            'cantidad' : forms.NumberInput(attrs={'class':'form-control'}),
        }

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        exclude = ['productos']
        fields = [
            'id',
            'id_funcionario',
            'id_recinto',
            'devolucion',
            'total',
            'productos',
        ]

        labels = {

            'id' : 'id entrega',
            'id_funcionario' : 'Funcionario',
            'id_recinto': 'Recinto',
            'devolucion': 'Devolución',
            'total' : 'Total',
            'productos': 'productos',
        }

        widgets = {
            'id_entrega' : forms.Select(attrs={'class':'form-control'}),
            'id_fun' : forms.Select(attrs={'class':'form-control'}),
            'id_rec' : forms.Select(attrs={'class':'form-control'}),
            'devolucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format="%Y-%m-%d"),
            'total' : forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly', 'id':'TotalSalida'}),
            'productos' : forms.Select(attrs={'class':'form-control'}),
        }

class Pre_prodForm(forms.ModelForm):
    class Meta:
        model = Pre_prod
        fields = [
            'id_prod',
            'id_prestamo',
            'precio',
            'cantidad',
        ]

        labels = {

            'id_prod' : 'Productos',
            'id_prestamo' : 'Prestamo',
            'precio': 'precio',
            'cantidad': 'cantidad',
        }

        widgets = {
            'id_prod' : forms.Select(attrs={'class':'form-control'}),
            'id_prestamo' : forms.Select(attrs={'class':'form-control'}),
            'precio' : forms.NumberInput(attrs={'class':'form-control'}),
            'cantidad' : forms.NumberInput(attrs={'class':'form-control'}),
        }


