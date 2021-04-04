from django.contrib.auth.decorators import login_required
from django.urls import path

from apps.empleado.views import *
from . import views

app_name = 'Clientes'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('reporte', login_required(report.as_view()), name='reporte'),
    path('rendimiento', login_required(report_rendimiento.as_view()), name='rendimiento'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('editar/<int:pk>', login_required(UpdateView.as_view()), name='editar'),
    path('eliminar/<int:pk>', login_required(DeleteView.as_view()), name='eliminar'),
    # path('ciudad', login_required(views.ciudad), name='ciudad'),
]
