"""citas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from apps import backEnd
from citas import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu', login_required(backEnd.menu), name='menu'),
    path('', login_required(backEnd.menu)),
    path('login', backEnd.logeo, name='login'),
    path('register', backEnd.cliente_add, name='register'),
    path('logout', login_required(backEnd.disconnect), name='logout'),
    path('connect/', backEnd.connect, name='connect'),
    path('verificar/', backEnd.check_ced, name='verificar'),
    path('equipos/', include('apps.maquina.urls', namespace='equipos')),
    path('categoria/', include('apps.categoria.urls', namespace='categoria')),
    path('presentacion/', include('apps.presentacion.urls', namespace='presentacion')),
    path('empleado/', include('apps.empleado.urls', namespace='empleado')),
    path('proveedor/', include('apps.proveedor.urls', namespace='proveedor')),
    path('producto/', include('apps.producto.urls', namespace='producto')),
    path('compra/', include('apps.compra.urls', namespace='compra')),
    path('transaccion/', include('apps.venta.urls', namespace='venta')),
    path('servicio/', include('apps.servicio.urls', namespace='servicio')),
    path('persona/', include('apps.user.urls', namespace='user')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
                  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
