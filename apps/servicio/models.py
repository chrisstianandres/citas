from django.db import models
from django.forms import model_to_dict

from apps.categoria.models import Categoria
from apps.maquina.models import Maquina
from citas.settings import MEDIA_URL


class Servicio(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    duracion = models.IntegerField(default=60)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, blank=True, null=True)
    imagen = models.ImageField(upload_to='servicio', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(MEDIA_URL, 'servicio/no_disponible.jpg')

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['duracion'] = self.duracion / 60
        item['precio'] = format(self.precio, '.2f')
        item['imagen'] = self.get_image()
        return item

    class Meta:
        db_table = 'servicio'
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'
        ordering = ['-id', '-nombre']

