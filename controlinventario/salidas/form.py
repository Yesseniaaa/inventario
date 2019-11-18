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
    id_recinto = forms.ModelMultipleChoiceField(label="Recinto",queryset=Recinto.objects.all().filter(estado=True).distinct().order_by('nombre'), widget=forms.CheckboxSelectMultiple())
	class Meta:
		model = Funcionario

		fields = {
			'rut',
			'nombres',
			'paterno',
			'materno',
			'mail',
			'telefono',
            'id_recinto',
		}

		labels = {
			'rut' : 'RUT',
			'nombres' : 'Nombres',
			'paterno' : 'Apellido Paterno',
			'materno' : 'Apellido Materno',
			'mail' : 'Mail',
			'telefono' : 'Teléfono',
            'id_recinto' : 'Recinto',
		}
        widgets = {
			'rut': forms.TextInput(attrs={'class': 'form-control rut', 'placeholder':'123456789-k'}),
			'nombres': forms.TextInput(attrs={'class': 'form-control'}),
			'paterno': forms.TextInput(attrs={'class': 'form-control'}),
			'materno': forms.TextInput(attrs={'class': 'form-control'}),
			'mail': forms.EmailInput(attrs={'class': 'form-control'}),
			'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
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
            'tipo',
            'productos',
        ]

        labels = {

            'id' : 'id entrega',
            'id_funcionario' : 'Funcionario',
            'id_recinto': 'Recinto',
            'total': 'total',
            'tipo': 'tipo',
            'productos': 'productos',
        }

        widgets = {
            'id_entrega' : forms.Select(attrs={'class':'form-control'}),
            'id_fun' : forms.Select(attrs={'class':'form-control'}),
            'id_rec' : forms.Select(attrs={'class':'form-control'}),
            'total' : forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly', 'id':'TotalSalida'}),
            'tipo' : forms.Select(attrs={'class':'form-control'}),
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
            'id_venta' : forms.Select(attrs={'class':'form-control'}),
            'precio' : forms.NumberInput(attrs={'class':'form-control'}),
            'cantidad' : forms.NumberInput(attrs={'class':'form-control'}),
        }

