from django.contrib import admin
from .models import *


class VentaAdmin(admin.TabularInline):
    model = Detalle_venta


class ServicioAdmin(admin.TabularInline):
    model = Detalle_servicios


class Detalle_ventaAdmin(admin.ModelAdmin):
    inlines = (VentaAdmin,)


class Detalle_servicioAdmin(admin.ModelAdmin):
    inlines = (ServicioAdmin,)


admin.site.register(Venta,  Detalle_servicioAdmin)

