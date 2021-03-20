from django import forms
from django.contrib.auth.models import Group
from django.forms import TextInput

from apps.producto.models import Producto


class ProductoForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['nombre'].widget = TextInput(
                attrs={'placeholder': 'Ingrese el nombre del producto', 'class': 'form-control',
                       'id': 'id_nombre_producto'})
            self.fields['descripcion'].widget = TextInput(
                attrs={'placeholder': 'Ingrese una descripcion del producto', 'class': 'form-control',
                       'id': 'id_descripcion_producto'})
            self.fields['categoria'].widget.attrs = {
                'class': 'form-control select2 input-sm',
                'id': 'id_categoria_producto'}
            self.fields['presentacion'].widget.attrs = {
                'class': 'form-control select2 input-sm'}

    class Meta:
        model = Producto
        fields = ['nombre',
                  'descripcion',
                  'categoria',
                  'presentacion',
                  'imagen'
                  ]
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Decripcion',
            'categoria': 'Categoria',
            'presentacion': 'Presentacion',
            'imagen': 'Imagen',
        }
        widgets = {
            'nombre': forms.TextInput(),
            'descripcion': forms.TextInput(),
            'decripcion': forms.Textarea(attrs={'col': '3', 'row': '2'})
        }



class GroupForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['name'].widget.attrs = {
                'class': 'form-control form-control-sm input-sm'}

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        labels = {'name': 'Nombre', 'permissions': 'Permisos'}
        widgets = {'name': forms.TextInput(),
                   'permissions': forms.SelectMultiple(attrs={
                       'class': 'form-control c',
                       'style': 'width: 100%',
                       'multiple': 'multiple'
                   })}
