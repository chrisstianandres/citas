from PIL import Image
from django import forms
from datetime import *

from django.db import transaction
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
                attrs={'class': 'form-control input-sm', 'value': ''})
            self.fields['precio'].widget = TextInput(
                attrs={'class': 'form-control input-sm', 'value': '1.00'})

        # habilitar, desabilitar, y mas

    class Meta:
        model = Servicio
        fields = ['nombre', 'categoria',
                  'descripcion', 'imagen', 'duracion', 'precio'
                  ]
        labels = {
            'nombre': 'Nombre', 'precio': 'Precio', 'categoria': 'Categoria',
            'descripcion': 'Decripcion', 'imagen': 'Imagen', 'duracion': 'Duracion (Maximo 4)'
        }
        widgets = {
            'nombre': forms.TextInput(),
            'duracion': forms.TextInput(attrs={'value': 1}),
            'precio': forms.TextInput(),
            'decripcion': forms.TextInput(attrs={'col': '3', 'row': '2'})
        }

    @transaction.atomic()
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                u = form.save(commit=False)
                if u.pk is None:
                    query = Servicio.objects.filter(nombre__icontains=self.cleaned_data['nombre'])
                else:
                    query = Servicio.objects.filter(nombre__icontains=self.cleaned_data['nombre']).exclude(id=u.pk)
                if query:
                    u.add_error("nombre", "Ya existe un servicio este nombre")
                    data['error'] = u.errors
                else:
                    dur = self.cleaned_data['duracion']
                    u.duracion = dur * 60
                    u.save()
                    data['resp'] = True
                image = Image.open(u.imagen)
                size = (1000, 500)
                image = image.resize(size, Image.ANTIALIAS)
                print(u.imagen.path)
                image.save(u.imagen.path)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
