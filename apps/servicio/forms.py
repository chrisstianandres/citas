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


        # habilitar, desabilitar, y mas

    class Meta:
        model = Servicio
        fields = ['nombre',
                  'descripcion'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Decripcion'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'decripcion': forms.Textarea(attrs={'col': '3', 'row': '2'})
        }
