from datetime import datetime
from django.db import models
from django.forms import model_to_dict

from apps.user.models import User
from apps.producto.models import Producto
from apps.presentacion.models import Presentacion
from apps.proveedor.models import Proveedor

estado = (
    (0, 'DEVUELTA'),
    (1, 'FINALIZADA')
)


class Compra(models.Model):
    fecha = models.DateField(default=datetime.now)
    comprobante = models.CharField(unique=True, max_length=100)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva_generado = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    tasa_iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.IntegerField(choices=estado, default=1)

    def __str__(self):
        return '%s %s' % (self.fecha, self.proveedor.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['proveedor'] = self.proveedor.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva_generado'] = format(self.iva_generado, '.2f')
        item['tasa_iva'] = format(self.tasa_iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['estado_text'] = self.get_estado_display()
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        return item

    class Meta:
        db_table = 'compra'
        verbose_name = 'compra'
        verbose_name_plural = 'compras'
        ordering = ['-id', 'proveedor']


class Detalle_compra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    precio_compra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    precio_venta = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    cantidad = models.IntegerField(default=1)
    stock_compra = models.IntegerField(default=1)
    stock_actual = models.IntegerField(default=1)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '{}{}'.format(self.compra, self.producto.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['compra'] = self.compra.toJSON()
        item['producto'] = self.producto.toJSON()
        item['precio_compra'] = format(self.precio_compra, '.2f')
        item['precio_venta'] = format(self.precio_venta, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        db_table = 'detalle_compra'
        verbose_name = 'detalle_compra'
        verbose_name_plural = 'detalles_compras'
        ordering = ['id', 'compra']