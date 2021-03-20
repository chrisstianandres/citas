from django.conf.urls import url
from django.urls import path
from . import views
from apps.proveedor.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Proveedor'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('editar/<int:pk>', login_required(ActualizarView.as_view()), name='editar'),
    path('eliminar/<int:pk>', login_required(EliminarView.as_view()), name='eliminar'),
    path('report', login_required(report.as_view()), name='report')
]
