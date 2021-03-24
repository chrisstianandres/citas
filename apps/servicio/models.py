from django.db import models
from django.forms import model_to_dict

from apps.categoria.models import Categoria
from apps.maquina.models import Maquina


class Servicio(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    duracion = models.IntegerField(default=30)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '%s' % self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['precio'] = format(self.precio, '.2f')
        return item

    class Meta:
        db_table = 'servicio'
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
        ordering = ['-id', '-nombre']

