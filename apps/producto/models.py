import os
from datetime import datetime
from io import BytesIO

import qrcode
from PIL import Image, ImageDraw
from django.core.files import File
from django.db import models
from django.forms import model_to_dict


from apps.categoria.models import Categoria
from apps.presentacion.models import Presentacion
from citas.settings import STATIC_URL, MEDIA_URL, BASE_DIR, SECRET_KEY_ENCRIPT, MEDIA_ROOT


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, null=True, blank=True)
    presentacion = models.ForeignKey(Presentacion, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='productos', blank=True, null=True)
    qr = models.ImageField(upload_to='productos/qr', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.nombre)

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(MEDIA_URL, 'productos/no_disponible.jpg')

    def get_qr(self):
        if self.qr:
            return '{}{}'.format(MEDIA_URL, self.qr)

    def get_qr_2(self):
        if self.qr:
            return '{}{}'.format(MEDIA_ROOT, self.qr)

    # def save(self, *args, **kwargs):
    #
    #     super().save(*args, *kwargs)

    def toJSON(self):
        item = model_to_dict(self)
        item['presentacion'] = self.presentacion.toJSON()
        item['categoria'] = self.categoria.toJSON()
        item['imagen'] = self.get_image()
        item['qr'] = self.get_qr()
        item['tipo'] = 'Producto'
        return item

    class Meta:
        db_table = 'producto'
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['-id']


class envio_stock_dia(models.Model):
    fecha = models.DateField(default=datetime.now(), unique=True)
    enviado = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.fecha.strftime('%Y-%m-%d'))
