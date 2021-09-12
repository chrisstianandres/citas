from django.conf.urls import url
from django.urls import path
from . import views
from apps.venta.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Venta'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('venta/nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('cita/nuevo', login_required(CitacrudView.as_view()), name='cita_nuevo'),
    path('nuevo_online', login_required(CrudViewOnline.as_view()), name='nuevo_online'),
    path('online', views.CrudView_online, name='online'),
    path('chart', login_required(views.grap), name='chart'),
    path('printpdf/<int:pk>', login_required(printpdf.as_view()), name='printpdf'),
    path('printQR', login_required(printQR.as_view()), name='printQR'),
    path('venta/report_productos', login_required(report.as_view()), name='report_by_product'),
    path('venta/report_services', login_required(report_servicios.as_view()), name='report_by_services'),
    path('venta/report_total', login_required(report_total.as_view()), name='report_total'),
    path('report_total_pedidos', login_required(report_total_reserva.as_view()), name='report_total_pedidos'),
    path('data_tarjets', login_required(views.data_tarjets), name='data_tarjets'),

]
