from django import forms
from django.http import HttpResponseRedirect
from salidas.models import Recinto, Funcionario
from .models import *

class ActivofijoForm(forms.ModelForm):
    id_funcionario = forms.ModelChoiceField(label='Funcionario', queryset=Funcionario.objects.all().filter(estado=True).distinct(), widget=forms.Select(attrs={'class':'form-control'}))
    id_recinto = forms.ModelChoiceField(label='Recinto', queryset=Recinto.objects.all().filter(estado=True).distinct(), widget=forms.Select(attrs={'class':'form-control'}))             
    class Meta:
        model = Activofijo
        exclude = ['estado']
        fields = [
            'nombre',
            'cod_barra',
            'descripcion',
        ]
        labels = {
            'nombre': 'Nombre',
            'cod_barra': 'Código de barra',
            'descripcion': 'Descripción',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'cod_barra': forms.NumberInput(attrs={'class':'form-control'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),
        }