from django import forms
from datetime import *
from .models import Compra, Detalle_compra


class CompraForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['fecha'].widget.attrs = {
                'readonly': True,
                'class': 'form-control datetimepicker',
                'data-date-format': 'yyyy-mm-dd',
            }

            self.fields['proveedor'].widget.attrs = {
                'class': 'form-control',

            }
            self.fields['subtotal'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }
            self.fields['iva_generado'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }
            self.fields['tasa_iva'].widget.attrs = {
                'value': 12.00,

            }
            self.fields['total'].widget.attrs = {
                'value': '0.00',
                'class': 'form-control',
                'readonly': True
            }

        # habilitar, desabilitar, y mas

    class Meta:
        model = Compra
        fields = [
            'fecha',
            'proveedor',
            'subtotal',
            'tasa_iva',
            'iva_generado',
            'total'
        ]
        labels = {
            'fecha': 'Fecha de Compra',
            'proveedor': 'Proveedor',
            'subtotal': 'Subtotal',
            'tasa_iva': 'I.V.A.',
            'iva_generado': 'I.V.A.',
            'total': 'TOTAL'
        }
        widgets = {
            'fecha': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            ),
            'tasa_iva': forms.TextInput(attrs={'value': '12'}),
            'iva_generado': forms.TextInput(),
            'total': forms.TextInput(),
        }


class Detalle_CompraForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            self.fields['producto'].widget.attrs = {
                'class': 'form-control select2',
                'data-live-search': "true"
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = Detalle_compra
        fields = [
            'producto'
        ]
