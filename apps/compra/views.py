import json
from datetime import datetime, timedelta

from django.db import transaction
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.compra.forms import CompraForm, Detalle_CompraForm
from apps.compra.models import Compra, Detalle_compra
from apps.devoluciones.models import Devolucion_compra
from apps.empresa.models import Empresa
from apps.producto.models import Producto
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.models import Producto
from datetime import date
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from apps.proveedor.forms import ProveedorForm
from apps.proveedor.models import Proveedor

opc_icono = 'fa fa-shopping-bag'
opc_entidad = 'Compras'
crud = '/compra/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Compra
    template_name = 'front-end/compra/list.html'
    permission_required = 'compra.view_compra'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Compra.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                start = request.POST['start_date']
                end = request.POST['end_date']
                if start and end:
                    compra = Compra.objects.filter(fecha_compra__range=[start, end])
                else:
                    compra = Compra.objects.all()
                for c in compra:
                    data.append(c.toJSON())
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    for p in Detalle_compra.objects.filter(compra_id=id):
                        item = p.toJSON()
                        data.append(item)
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'devolucion':
                id = request.POST['id']
                key = 0
                ahora = datetime.now()
                dev = self.model.objects.get(id=id)
                fechaCadena = str(dev.fecha) + " 00:00:00"
                fecha = datetime.strptime(fechaCadena, '%Y-%m-%d %H:%M:%S')
                if ahora > (fecha + timedelta(days=1)):
                    data['error'] = 'Solo puede anular las compras maximo 1 dia despues de la transaccion'
                else:
                    for det in dev.detalle_compra_set.all():
                        if det.stock_actual < det.stock_compra:
                            key = 1
                            data['error'] = 'Imposible anular la compra <br> Los productos ya fueron utilizados'
                        break
                    if key == 0:
                        dev.estado = 0
                        dev.save()
                        add = Devolucion_compra()
                        add.compra_id = id
                        add.save()
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Compra'
        data['titulo'] = 'Listado de Compras'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Compra
    template_name = 'front-end/compra/form.html'
    permission_required = 'compra.add_compra'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                datos = json.loads(request.POST['compras'])
                if datos:
                    with transaction.atomic():
                        c = Compra()
                        c.fecha_compra = datos['fecha']
                        c.comprobante = int(datos['comprobante'])
                        c.proveedor_id = int(datos['proveedor'])
                        c.subtotal = float(datos['subtotal'])
                        c.tasa_iva = float(datos['tasa_iva'])
                        c.iva_generado = c.subtotal-c.total
                        c.total = float(datos['total'])
                        c.save()
                        for i in datos['productos']:
                            dv = Detalle_compra()
                            dv.compra_id = c.id
                            dv.producto_id = int(i['id'])
                            dv.precio_compra = float(i['precio'])
                            dv.precio_venta = float(i['pvp'])
                            dv.cantidad = int(i['cantidad'])
                            dv.stock_compra = int(i['cantidad'])
                            dv.stock_actual = int(i['cantidad'])
                            dv.subtotal = float(i['subtotal'])
                            dv.save()
                        data['id'] = c.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'get_prov':
                data = []
                id = request.POST['id']
                query = Proveedor.objects.get(id=id)
                data.append(query.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Compra'
        data['titulo'] = 'Nueva Compra'
        data['nuevo'] = '/compra/nuevo'
        data['empresa'] = empresa
        data['form'] = CompraForm()
        data['form2'] = Detalle_CompraForm()
        data['detalle'] = []
        data['formp'] = ProveedorForm()
        return data


@csrf_exempt
def index(request):
    data = {}
    try:
        data = []
        h = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)
        for p in Detalle_compra.objects.filter(compra__fecha_compra__range=[h, h + timedelta(days=6)],
                                               compra__estado=1):
            data.append(p.toJSON())
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


class printpdf(ValidatePermissionRequiredMixin, View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path = result[0]
        else:
            sUrl = settings.STATIC_URL  # Typically /static/
            sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL  # Typically /media/
            mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def pvp_cal(self, *args, **kwargs):
        data = []
        try:
            iva_emp = Empresa.objects.get(pk=1)
            for i in Detalle_compra.objects.filter(compra_id=self.kwargs['pk']):
                item = i.compra.toJSON()
                item['producto'] = i.producto.toJSON()
                item['pvp'] = format(i.p_compra_actual, '.2f')
                item['cantidad'] = i.cantidad
                item['subtotal'] = format(i.subtotal, '.2f')
                data.append(item)
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/pdf_compra.html')
            context = {'title': 'Comprobante de Compra',
                       'sale': Compra.objects.get(pk=self.kwargs['pk']),
                       'det_sale': self.pvp_cal(),
                       'empresa': Empresa.objects.get(id=1),
                       'icon': 'media/logo_don_chuta.png'
                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('compra:lista'))


class report(ValidatePermissionRequiredMixin, ListView):
    model = Compra
    template_name = 'front-end/compra/report_product.html'
    permission_required = 'compra.view_compra'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Compra.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                if start_date == '' and end_date == '':
                    query = Detalle_compra.objects.filter(compra__estado=1).values('compra__fecha', 'producto__nombre',
                                                          'precio_compra'). \
                        order_by().annotate(Sum('cantidad')).annotate(Sum('compra__total')).annotate(Sum('subtotal'))
                else:
                    query = (Detalle_compra.objects.filter(compra__estado=1).values('compra__fecha', 'producto__nombre',
                                                           'precio_compra').
                        filter(compra__fecha__range=[start_date, end_date]).order_by().annotate(
                        Sum('cantidad'))).annotate(Sum('compra__total'))
                for p in query:
                    data.append([
                        p['compra__fecha'].strftime("%d/%m/%Y"),
                        p['producto__nombre'],
                        int(p['cantidad__sum']),
                        format(p['precio_compra'], '.2f'),
                        format(p['compra__total__sum'], '.2f')])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Compras'
        data['empresa'] = empresa
        return data


class report_total(ValidatePermissionRequiredMixin, ListView):
    model = Compra
    template_name = 'front-end/compra/report_total.html'
    permission_required = 'compra.view_compra'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Compra.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Compra.objects.filter(estado=1).values('fecha', 'proveedor__nombre',).annotate(Sum('total'))
                else:
                    query = Compra.objects.filter(estado=1).values('fecha', 'proveedor__nombre').filter(
                        fecha__range=[start_date, end_date]).annotate(Sum('total'))
                for p in query:
                    data.append([
                        p['fecha'].strftime("%d/%m/%Y"),
                        p['proveedor__nombre'],
                        format(p['total__sum'], '.2f')
                    ])
            else:
                data['error'] = 'No ha seccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Compras Totales'
        data['empresa'] = empresa
        return data
