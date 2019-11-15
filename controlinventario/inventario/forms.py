from django import forms
from .models import *


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
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

class ProductoFormUpdate(forms.ModelForm):
    #id_cat = forms.ModelChoiceField(queryset=Categoria.objects.values_list('nombre', flat=True).filter(estado=True).distinct(),widget=forms.Select(attrs={'class': 'form-control'}))
    #id_cat = forms.ModelChoiceField(label='Categoria', queryset=Categoria.objects.all().filter(estado=True).distinct(), widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control'}))
    id_cat = forms.ModelMultipleChoiceField(label="Categoria",queryset=Categoria.objects.all().filter(estado=True).distinct().order_by('nombre'), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'cod_barra',
            'stock_min',
            'descripcion',
            'id_cat',
        ]
        labels = {
            'nombre': 'Nombre',
            'cod_barra': 'Código de barra',
            'stock_min': 'Stock mínimo',
            'descripcion': 'Descripción',
            'id_cat': 'Categoria',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'cod_barra': forms.NumberInput(attrs={'class':'form-control'}),
            'stock_min': forms.NumberInput(attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),
            'id_cat': forms.CheckboxSelectMultiple(),
        }