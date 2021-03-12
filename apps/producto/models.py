from django.db import models
from django.forms import model_to_dict

from apps.categoria.models import Categoria
from apps.presentacion.models import Presentacion
from citas.settings import STATIC_URL


class Producto(models.Model):
    caategoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        item['presentacion'] = self.presentacion.toJSON()
        item['caategoria'] = self.caategoria.toJSON()
        return item

    class Meta:
        db_table = 'producto'
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-id']