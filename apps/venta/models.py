from datetime import datetime

from django.db import models
from django.forms import model_to_dict


from apps.compra.models import Detalle_compra
from apps.empleado.models import Empleado
from apps.maquina.models import Maquina
from apps.servicio.models import Servicio

from apps.producto.models import Producto
from apps.user.models import User
from apps.empresa.models import Empresa

estado = (
    (0, 'ANULADA'),
    (1, 'FINALIZADA'),
    (2, 'RESERVADA')
)


class Venta(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, null=True, blank=True)
    fecha_factura = models.DateField(default=datetime.now)
    fecha_reserva = models.DateField(default=datetime.now)
    duracion_servicio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    hora_inicio = models.IntegerField(default=0)
    minuto_inicio = models.IntegerField(default=0)
    hora_fin = models.IntegerField(default=0)
    minuto_fin = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    estado = models.IntegerField(choices=estado, default=1)
    citacancelada = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s' % (self.user.get_full_name(), self.fecha_factura, self.total)

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['estado_text'] = self.get_estado_display()
        item['fecha_factura'] = self.fecha_factura.strftime('%Y-%m-%d')
        item['fecha_reserva'] = self.fecha_reserva.strftime('%Y-%m-%d')
        item['duracion_servicio'] = format(self.duracion_servicio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    def get_servicios(self):
        data = []
        for servicio in self.detalle_servicios_set.all():
            item = servicio.toJSON()
            data.append(item)
        return data

    class Meta:
        db_table = 'venta'
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'


class Detalle_venta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT)
    det_compra = models.ForeignKey(Detalle_compra, on_delete=models.PROTECT)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s' % self.venta

    def toJSON(self):
        empresa = Empresa.objects.first()
        item = model_to_dict(self)
        item['venta'] = self.venta.toJSON()
        item['det_compra'] = self.det_compra.toJSON()
        return item

    class Meta:
        db_table = 'detalle_venta'
        verbose_name = 'detalle_venta'
        verbose_name_plural = 'detalles_ventas'


class Detalle_servicios(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT)
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, null=True, blank=True, default=None)
    valor = models.DecimalField(default=1.00, max_digits=9, decimal_places=2, blank=True, null=True)
    cantidad = models.IntegerField(default=0)
    subtotals = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return '%s' % (self.venta)

    def toJSON(self):
        item = model_to_dict(self)
        item['venta'] = self.venta.toJSON()
        item['servicio'] = self.servicio.toJSON()
        item['empleado'] = self.empleado.toJSON()
        item['valor'] = format(self.valor, '.2f')
        item['subtotals'] = format(self.subtotals, '.2f')
        return item

    class Meta:
        db_table = 'detalle_venta_servicio'
        verbose_name = 'detalle_venta_servicio'
        verbose_name_plural = 'detalles_venta_servicios'


class Detalle_maquinas(models.Model):
    servicio = models.ForeignKey(Detalle_servicios, on_delete=models.PROTECT)
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)

    def __str__(self):
        return '{}'.format(self.maquina.tipo.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['maquina'] = self.maquina.toJSON()
        return item

    class Meta:
        db_table = 'detalle_venta_maquina'
        verbose_name = 'detalle_venta_maquina'
        verbose_name_plural = 'detalles_venta_maquina'
