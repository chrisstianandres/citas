from django.db import models
from django.forms import model_to_dict

from apps.maquina.models import Maquina


class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    duracion = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'servicio'
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
        ordering = ['-id', '-nombre']


class Detalle_maquinas(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, null=True, blank=True, default=None)
    maquina = models.ForeignKey(Maquina, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.servicio, self.maquina)

    def toJSON(self):
        item = model_to_dict(self)
        item['maquina'] = self.maquina.toJSON()
        item['serivicio'] = self.servicio.toJSON()
        return item

    class Meta:
        db_table = 'detalle_maquina'
        verbose_name = 'detalle_maquina'
        verbose_name_plural = 'detalle_maquinas'
