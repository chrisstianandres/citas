from django.db import models
from django.forms import model_to_dict

from apps.categoria.models import Categoria
from apps.presentacion.models import Presentacion
from citas.settings import STATIC_URL, MEDIA_URL


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(MEDIA_URL, 'productos/no_disponible.jpg')

    def toJSON(self):
        item = model_to_dict(self)
        item['presentacion'] = self.presentacion.toJSON()
        item['categoria'] = self.categoria.toJSON()
        item['imagen'] = self.get_image()
        item['tipo'] = 'Producto'
        return item

    class Meta:
        db_table = 'producto'
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-id']