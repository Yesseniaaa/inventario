from django import forms

from adquisiciones.models import MermaM
from salidas.models import Recinto
from .models import *


class MermaForm(forms.ModelForm):
    id_producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(), empty_label=None, label="Productos"
    )

    class Meta:
        model = MermaM
        fields = ['id_producto','cantidad','observaciones']


class Reporte1Form(forms.ModelForm):
    producto_id = forms.ModelChoiceField(
        queryset=Producto.objects.all(), empty_label=None, label="Productos"
    )

    fecha_inicio = forms.DateField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"),
    )
    fecha_fin = forms.DateField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"),
    )

    class Meta:
        model = Producto
        fields = ["producto_id", "fecha_inicio", "fecha_fin"]


class Reporte2Form(forms.ModelForm):
    recinto_id = forms.ModelChoiceField(
        queryset=Recinto.objects.all(), empty_label=None, label="Recinto"
    )

    fecha_inicio = forms.DateField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"),
    )
    fecha_fin = forms.DateField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"),
    )

    class Meta:
        model = Recinto
        fields = ["recinto_id", "fecha_inicio", "fecha_fin"]


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = [
            "nombre",
            "descripcion",
        ]
        labels = {"nombre": "Nombre", "descripcion": "Descripción"}
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
        }


class ProductoFormUpdate(forms.ModelForm):
    # id_cat = forms.ModelChoiceField(queryset=Categoria.objects.values_list('nombre', flat=True).filter(estado=True).distinct(),widget=forms.Select(attrs={'class': 'form-control'}))
    # id_cat = forms.ModelChoiceField(label='Categoria', queryset=Categoria.objects.all().filter(estado=True).distinct(), widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control'}))
    id_cat = forms.ModelMultipleChoiceField(
        label="Categoria",
        queryset=Categoria.objects.all().filter(estado=True).distinct().order_by("nombre"),
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Producto
        fields = [
            "nombre",
            "cod_barra",
            "stock_min",
            "descripcion",
            "id_cat",
        ]
        labels = {
            "nombre": "Nombre",
            "cod_barra": "Código de barra",
            "stock_min": "Stock mínimo",
            "descripcion": "Descripción",
            "id_cat": "Categoria",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "cod_barra": forms.NumberInput(attrs={"class": "form-control"}),
            "stock_min": forms.NumberInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "id_cat": forms.CheckboxSelectMultiple(),
        }
