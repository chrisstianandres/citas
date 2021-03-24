from datetime import datetime

from django import forms

from .models import Detalle_venta, Venta
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
            self.fields['duracion_servicio'].widget.attrs = {
                'class': 'form-control input-sm'
            }
            self.fields['fecha_factura'].initial = datetime.now().strftime('%Y-%m-%d')
            self.fields['user'].widget.attrs = {
                'class': 'form-control'
            }
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
            'user',
            'duracion_servicio',
            'subtotal',
            'iva',
            'total'
        ]
        labels = {
            'fecha_factura': 'Fecha de Venta',
            'user': 'Cliente',
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
