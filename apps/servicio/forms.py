from django import forms
from datetime import *
from django.forms import SelectDateWidget, TextInput, NumberInput, EmailInput

from .models import Servicio


class ServicioForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del Servicio', 'class': 'form-control form-rounded'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una descripcion del Servicio', 'class': 'form-control form-rounded'})
            self.fields['duracion'].widget = TextInput(
                attrs={'class': 'form-control input-sm'})
            self.fields['precio'].widget = TextInput(
                attrs={'class': 'form-control input-sm', 'value': '1.00'})


        # habilitar, desabilitar, y mas

    class Meta:
        model = Servicio
        fields = ['nombre', 'categoria',
                  'descripcion', 'duracion', 'precio'
                  ]
        labels = {
            'nombre': 'Nombre', 'precio': 'Precio', 'categoria': 'Categoria',
            'descripcion': 'Decripcion', 'duracion': 'Duracion (Maximo 60)'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'duracion': forms.TextInput(),
            'precio': forms.TextInput(),
            'decripcion': forms.TextInput(attrs={'col': '3', 'row': '2'})
        }
