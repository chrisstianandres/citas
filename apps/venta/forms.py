from datetime import datetime

from django import forms

from .models import Venta, Detalle_servicios
from ..empleado.models import Empleado
from ..user.models import User


class VentaForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha_factura'].widget.attrs = {
                'readonly': True,
                'class': 'form-control',
                'id': 'id_fecha_venta',
            }
            self.fields['fecha_reserva'].widget.attrs = {
                'class': 'form-control',
                'id': 'id_fecha_reserva',
                'autocomplete': 'off',
                'readonly': True
            }
            self.fields['duracion_servicio'].widget.attrs = {
                'class': 'form-control input-sm'
            }
            self.fields['fecha_factura'].initial = datetime.now().strftime('%Y-%m-%d')
            self.fields['fecha_reserva'].initial = ''
            self.fields['user'].widget.attrs = {'class': 'form-control'}
            self.fields['empleado'].widget.attrs = {'class': 'form-control'}
            self.fields['user'].queryset = User.objects.filter(tipo=0)
            self.fields['subtotal'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }
            self.fields['iva'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }
            self.fields['total'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }

        # habilitar, desabilitar, y mas

    class Meta:
        model = Venta
        fields = [
            'fecha_factura',
            'fecha_reserva',
            'user',
            'empleado',
            'duracion_servicio',
            'subtotal',
            'iva',
            'total'
        ]
        labels = {
            'fecha_factura': 'Fecha de Venta',
            'fecha_reserva': 'Fecha',
            'user': 'Cliente',
            'empleado': 'Empleado',
            'duracion_servicio': 'Duracion de antencion',
            'subtotal': 'Subtotal',
            'iva': 'I.V.A.',
            'total': 'TOTAL'
        }
        widgets = {
            'fecha_factura': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'duracion_servicio ': forms.TextInput(),
        }


class Detalle_servicioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields['empleado'].widget.attrs = {'class': 'form-control', 'disabled': True}
            self.fields['empleado'].queryset = Empleado.objects.filter(estado=0)
            self.fields['servicio'].widget.attrs = {'class': 'form-control ct', 'multiple': 'multiple', 'placeholder_text_multiple': 'Selecciona uno o mas servicios....'}
            self.fields['servicio'].empty_label = None
        # habilitar, desabilitar, y mas
    class Meta:
        model = Detalle_servicios
        fields = [
            'empleado',
            'servicio'
        ]
        labels = {
            'empleado': 'Empleado',
            'servicio': 'Servicio'
        }
        widgets = {
            'servicio': forms.SelectMultiple()
        }
