import json
import os
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.staticfiles import finders
from django.db import transaction
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from xhtml2pdf import pisa

from apps.backEnd import nombre_empresa, verificar, send_email
from apps.compra.models import Compra, Detalle_compra
from apps.devoluciones.models import Devolucion_venta
from apps.empleado.models import Empleado
from apps.empresa.models import Empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.models import Producto
from apps.servicio.models import Servicio
from apps.user.forms import UserForm, UserForm_cliente
from apps.user.models import User
from apps.venta.forms import VentaForm, Detalle_servicioForm
from apps.venta.models import Venta, Detalle_venta, Detalle_servicios

opc_icono = 'fa fa-shopping-basket '
opc_entidad = 'Ventas'
crud = '/venta/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/list.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                start = request.POST['start_date']
                end = request.POST['end_date']
                data = []
                if start == '' and end == '':
                    if request.user.tipo == 1:
                        query = Venta.objects.all()
                    else:
                        query = Venta.objects.filter(user_id=request.user.id)
                else:
                    if request.user.tipo == 1:
                        query = Venta.objects.filter(fecha_factura__range=[start, end])
                    else:
                        query = Venta.objects.filter(user_id=request.user.id,
                                                     fecha_factura__range=[start, end])
                for c in query:
                    data.append(c.toJSON())
            elif action == 'detalle':
                id = request.POST['id']
                if id:
                    data = []
                    result = Detalle_venta.objects.values('det_compra__producto_id', 'pvp', 'subtotal').filter(
                        venta_id=id). \
                        annotate(cantidad=Sum('cantidad')).order_by('cantidad')
                    result2 = Detalle_servicios.objects.filter(venta_id=id)
                    for p1 in result:
                        p = Producto.objects.get(id=p1['det_compra__producto_id'])
                        data.append({
                            'nombre': p.nombre,
                            'tipo': 'Producto',
                            'duracion': 'N/A',
                            'categoria': p.categoria.nombre,
                            'presentacion': p.presentacion.nombre,
                            'cantidad': p1['cantidad'],
                            'precio': p1['pvp'],
                            'subtotal': p1['subtotal'],
                        })
                    for s in result2:
                        data.append({
                            'nombre': s.servicio.nombre,
                            'tipo': 'Servicio',
                            'duracion': s.servicio.duracion,
                            'categoria': s.servicio.categoria.nombre,
                            'presentacion': 'N/A',
                            'cantidad': s.cantidad,
                            'precio': s.valor,
                            'subtotal': s.subtotals,
                        })
            elif action == 'estado':
                id = request.POST['id']
                if id:
                    with transaction.atomic():
                        es = Venta.objects.get(id=id)
                        es.estado = 0
                        dev = Devolucion_venta()
                        dev.venta_id = id
                        dev.fecha = datetime.now()
                        dev.save()
                        for i in Detalle_venta.objects.filter(venta_id=id):
                            i.det_compra.stock_actual += i.cantidad
                            i.save()
                        es.save()
                        data['resp'] = True
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        if self.request.user.tipo == 0:
            data['entidad'] = 'Compras'
            data['boton'] = 'Nueva Compra'
            data['titulo'] = 'Listado de Compras realizadas'
        else:
            data['entidad'] = opc_entidad
            data['boton'] = 'Nueva Venta'
            data['titulo'] = 'Listado de Ventas'
            data['nuevo'] = '/transaccion/venta/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = VentaForm
    model = Venta
    template_name = 'front-end/venta/form.html'
    permission_required = 'venta.add_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                datos = json.loads(request.POST['ventas'])
                if datos:
                    with transaction.atomic():
                        c = self.model()
                        c.fecha_factura = datos['fecha']
                        c.fecha_reserva = datos['fecha']
                        c.user_id = datos['cliente']
                        c.empleado_id = datos['empleado']
                        c.duracion_servicio = datos['duracion']
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.save()
                        if datos['detalle']:
                            ids_p = []
                            for i in datos['detalle']:
                                if i['tipo'] == 'Producto':
                                    dv = Detalle_venta()
                                    dv.venta_id = c.id
                                    if Detalle_compra.objects.filter(producto_id=int(i['id']), compra__estado=1,
                                                                     stock_actual__gte=int(i['cantidad'])).exists():
                                        for det in Detalle_compra.objects.filter(producto_id=int(i['id']),
                                                                                 compra__estado=1,
                                                                                 stock_actual__gte=int(i['cantidad'])):
                                            dv = Detalle_venta()
                                            dv.venta_id = c.id
                                            dv.det_compra_id = det.id
                                            dv.cantidad = int(i['cantidad'])
                                            dv.pvp = float(i['precio'])
                                            dv.subtotal = float(i['subtotal'])
                                            dv.save()
                                            det.stock_actual -= int(i['cantidad'])
                                            det.save()
                                            if det.stock_actual <= 3:
                                                ids_p.append(det.producto.id)
                                            break
                                    else:
                                        cantidad = int(i['cantidad'])
                                        aux = cantidad
                                        for d in Detalle_compra.objects.filter(producto_id=int(i['id']),
                                                                               compra__estado=1):
                                            if cantidad > 0 and d.stock_actual > 0:
                                                aux -= d.stock_actual  # 15
                                                if aux >= 1:
                                                    dv = Detalle_venta()
                                                    dv.venta_id = c.id
                                                    dv.det_compra_id = d.id
                                                    dv.cantidad = cantidad - aux
                                                    dv.pvp = float(i['precio'])
                                                    dv.subtotal = float(i['subtotal'])
                                                    dv.save()
                                                    d.stock_actual -= (cantidad - aux)
                                                    d.save()
                                                    cantidad = aux  # 15
                                                else:
                                                    dv = Detalle_venta()
                                                    dv.venta_id = c.id
                                                    dv.det_compra_id = d.id
                                                    dv.cantidad = cantidad
                                                    dv.pvp = float(i['precio'])
                                                    dv.subtotal = float(i['subtotal'])
                                                    dv.save()
                                                    d.stock_actual -= cantidad
                                                    d.save()
                                                    cantidad = 0
                                                if d.stock_actual <= 3:
                                                    ids_p.append(d.producto.id)
                                else:
                                    ds = Detalle_servicios()
                                    ds.venta_id = c.id
                                    ds.empleado_id = int(i['empleado']['id'])
                                    ds.servicio_id = int(i['id'])
                                    ds.valor = float(i['precio'])
                                    ds.cantidad = int(i['cantidad'])
                                    ds.subtotals = float(i['subtotal'])
                                    ds.save()
                        if len(ids_p) > 0:
                            repor = []
                            for p in Producto.objects.filter(id__in=ids_p):
                                stock = Detalle_compra.objects.filter(compra__estado=1, producto_id=p.id).aggregate(
                                    stock=Coalesce(Sum('stock_actual'), 0)).get('stock')
                                if stock <= 10:
                                    item = p.toJSON()
                                    item['stock'] = stock
                                    repor.append(item)
                            if len(repor) > 0:
                                send_email(repor)
                        data['id'] = c.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'cita_factura':
                datos = json.loads(request.POST['ventas'])
                if datos:
                    with transaction.atomic():
                        c = self.model.objects.get(id=datos['venta'])
                        c.estado = 1
                        c.fecha_factura = datos['fecha']
                        c.duracion_servicio = datos['duracion']
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.save()
                        if datos['detalle']:
                            Detalle_servicios.objects.get(venta_id=c.id).delete()
                            for i in datos['detalle']:
                                if i['tipo'] == 'Producto':
                                    if Detalle_compra.objects.filter(producto_id=int(i['id']), compra__estado=1,
                                                                     stock_actual__gte=int(i['cantidad'])).exists():
                                        for det in Detalle_compra.objects.filter(producto_id=int(i['id']),
                                                                                 compra__estado=1,
                                                                                 stock_actual__gte=int(i['cantidad'])):
                                            dv = Detalle_venta()
                                            dv.venta_id = c.id
                                            dv.det_compra_id = det.id
                                            dv.cantidad = int(i['cantidad'])
                                            dv.pvp = float(i['precio'])
                                            dv.subtotal = float(i['subtotal'])
                                            dv.save()
                                            det.stock_actual -= int(i['cantidad'])
                                            det.save()
                                            break
                                    else:
                                        cantidad = int(i['cantidad'])
                                        aux = cantidad
                                        for d in Detalle_compra.objects.filter(producto_id=int(i['id']),
                                                                               compra__estado=1):
                                            if cantidad > 0 and d.stock_actual > 0:
                                                aux -= d.stock_actual  # 15
                                                if aux >= 1:
                                                    dv = Detalle_venta()
                                                    dv.venta_id = c.id
                                                    dv.det_compra_id = d.id
                                                    dv.cantidad = cantidad - aux
                                                    dv.pvp = float(i['precio'])
                                                    dv.subtotal = float(i['subtotal'])
                                                    dv.save()
                                                    d.stock_actual -= (cantidad - aux)
                                                    d.save()
                                                    cantidad = aux  # 15
                                                else:
                                                    dv = Detalle_venta()
                                                    dv.venta_id = c.id
                                                    dv.det_compra_id = d.id
                                                    dv.cantidad = cantidad
                                                    dv.pvp = float(i['precio'])
                                                    dv.subtotal = float(i['subtotal'])
                                                    dv.save()
                                                    d.stock_actual -= cantidad
                                                    d.save()
                                                    cantidad = 0
                                else:
                                    ds = Detalle_servicios()
                                    ds.venta_id = c.id
                                    ds.empleado_id = int(i['empleado']['id'])
                                    ds.servicio_id = int(i['id'])
                                    ds.valor = float(i['precio'])
                                    ds.cantidad = int(i['cantidad'])
                                    ds.subtotals = float(i['subtotal'])
                                    ds.save()
                        data['id'] = c.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'search_prod':
                data = []
                ids = json.loads(request.POST['ids'])
                query = Detalle_compra.objects.values('producto_id', 'precio_venta').filter(compra__estado=1). \
                    annotate(stock=Sum('stock_actual')) \
                    .order_by('stock').filter(stock_actual__gte=1)
                for c in query.exclude(producto_id__in=ids):
                    pro = Producto.objects.get(id=c['producto_id'])
                    item = pro.toJSON()
                    item['stock'] = c['stock']
                    item['id_det'] = pro.id
                    item['precio_venta'] = format(c['precio_venta'], '.2f')
                    data.append(item)
            elif action == 'search_serv':
                data = []
                ids = json.loads(request.POST['ids'])
                query = Servicio.objects.all()
                for p in query.exclude(id__in=ids):
                    item = p.toJSON()
                    item['tipo'] = 'Servicio'
                    data.append(item)
            elif action == 'search_empleados':
                data = []
                ids = json.loads(request.POST['ids'])
                query = Empleado.objects.all()
                for p in query.exclude(id__in=ids):
                    item = p.toJSON()
                    item['sexo'] = p.get_sexo_display()
                    data.append(item)
            elif action == 'save_user':
                f = UserForm_cliente(request.POST)
                datos = request.POST
                data = self.save_data(f, datos)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f, datos):
        data = {}
        if f.is_valid():
            if verificar(f.data['cedula']):
                use = User()
                use.username = datos['cedula']
                use.cedula = datos['cedula']
                use.first_name = datos['first_name']
                use.last_name = datos['last_name']
                use.sexo = datos['sexo']
                use.email = datos['email']
                use.telefono = datos['telefono']
                use.celular = datos['celular']
                use.direccion = datos['direccion']
                use.tipo = 0
                use.password = make_password(datos['cedula'])
                use.save()
                data['resp'] = True
                data = use.toJSON()
            else:
                f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                data['error'] = f.errors
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Venta'
        data['titulo'] = 'Nueva Venta'
        data['nuevo'] = '/venta/nuevo'
        data['titulo_factuta'] = 'Nueva Venta'
        data['empresa'] = empresa
        data['form'] = self.form_class()
        data['detalle'] = []
        data['formp'] = UserForm_cliente()
        data['formc'] = UserForm()
        return data


class CitacrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = VentaForm
    second_form_class = Detalle_servicioForm
    model = Venta
    template_name = 'front-end/cita/form.html'
    permission_required = 'venta.add_venta'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                datos = json.loads(request.POST['cita'])
                if datos:
                    with transaction.atomic():
                        c = self.model()
                        c.user_id = datos['cliente']
                        c.fecha_factura = datos['fecha_reserva']
                        c.fecha_reserva = datos['fecha_reserva']
                        c.duracion_servicio = int(datos['duracion'])
                        c.hora_inicio = datos['hora_inicio']
                        c.minuto_inicio = datos['minuto_inicio']
                        c.hora_fin = datos['hora_fin']
                        c.minuto_fin = datos['minuto_fin']
                        c.estado = 2
                        c.save()
                        for ser in datos['servicio'][0]:
                            dts = Detalle_servicios()
                            dts.venta_id = c.id
                            dts.servicio_id = int(ser)
                            dts.empleado_id = datos['empleado']
                            dts.valor = dts.servicio.precio
                            dts.cantidad = int(datos['empleado'])
                            dts.save()
                        data['id'] = c.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            elif action == 'search_citas':
                data = []
                query = Detalle_servicios.objects.filter(venta__estado=2)
                for c in query:
                    cita = Venta.objects.get(id=c.venta.id)
                    if cita.fecha_reserva < datetime.now().date() and cita.citacancelada == False:
                        cita.citacancelada = True
                        cita.save()
                    elif cita.fecha_reserva == datetime.now().date() and cita.hora_fin < datetime.now().hour and cita.minuto_fin < datetime.now().minute and cita.citacancelada == False:
                        cita.citacancelada = True
                        cita.save()
                    item = c.toJSON()
                    item['servicios'] = cita.get_servicios()
                    item['classname'] = 'label-success'
                    data.append(item)
            elif action == 'search_citas_cliente':
                data = []
                query = Detalle_servicios.objects.filter(venta__estado=2, venta__user_id=request.user.id)
                for c in query:
                    item = c.toJSON()
                    item['classname'] = 'label-info'
                    data.append(item)
            elif action == 'search_horario_empleado':
                data = []
                id = request.POST['id']
                query = Detalle_servicios.objects.filter(empleado_id=id, venta__estado=2,
                                                         venta__fecha_reserva__gte=datetime.now())
                for p in query:
                    item = p.toJSON()
                    item['fecha_factura'] = p.venta.fecha_factura.strftime('%m/%d/%Y')
                    item['fecha_reserva'] = p.venta.fecha_reserva.strftime('%m/%d/%Y')
                    data.append(item)
            elif action == 'search_horario_empleado_edit':
                data = []
                id = request.POST['id']
                exclude = request.POST['exclude']
                query = Detalle_servicios.objects.filter(empleado_id=id, venta__estado=2,
                                                         venta__fecha_reserva__gte=datetime.now()). \
                    exclude(venta_id=exclude)
                for p in query:
                    item = p.toJSON()
                    item['fecha_factura'] = p.venta.fecha_factura.strftime('%m/%d/%Y')
                    item['fecha_reserva'] = p.venta.fecha_reserva.strftime('%m/%d/%Y')
                    data.append(item)
            elif action == 'search_servicio_cita':
                data = []
                ids = json.loads(request.POST['ids'])
                query = Servicio.objects.filter(id__in=ids)
                dur = 0
                for p in query:
                    item = p.toJSON()
                    dur += p.duracion
                data = {'duracion': dur/60}
            elif action == 'edit_event':
                data = []
                id = request.POST['id']
                query = Detalle_servicios.objects.get(venta_id=id)
                data.append(query.toJSON())
            elif action == 'edit':
                id = request.POST['id']
                datos = json.loads(request.POST['cita'])
                if datos:
                    with transaction.atomic():
                        dts = Detalle_servicios.objects.get(id=id)
                        dts.venta_id = dts.venta.id
                        dts.servicio_id = datos['servicio']
                        dts.empleado_id = datos['empleado']
                        dts.save()
                        c = self.model.objects.get(id=dts.venta.id)
                        c.user_id = datos['cliente']
                        c.fecha_factura = datos['fecha_reserva']
                        c.fecha_reserva = datos['fecha_reserva']
                        c.duracion_servicio = datos['duracion']
                        c.hora_inicio = datos['hora_inicio']
                        c.hora_fin = datos['hora_fin']
                        c.estado = 2
                        c.save()
                        data['resp'] = True
            elif action == 'anular':
                id = request.POST['id']
                serv = Detalle_servicios.objects.get(id=id)
                vent = self.model.objects.get(id=serv.venta.id)
                vent.estado = 0
                vent.save()
            elif action == 'save_user':
                f = UserForm_cliente(request.POST)
                datos = request.POST
                data = self.save_data(f, datos)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f, datos):
        data = {}
        if f.is_valid():
            if verificar(f.data['cedula']):
                use = User()
                use.username = datos['cedula']
                use.cedula = datos['cedula']
                use.first_name = datos['first_name']
                use.last_name = datos['last_name']
                use.sexo = datos['sexo']
                use.email = datos['email']
                use.telefono = datos['telefono']
                use.celular = datos['celular']
                use.direccion = datos['direccion']
                use.tipo = 0
                use.password = make_password(datos['cedula'])
                use.save()
                data['resp'] = True
                data = use.toJSON()
            else:
                f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                data['error'] = f.errors
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-calendar'
        data['entidad'] = 'Agenda'
        data['boton'] = 'Guardar Cita'
        data['titulo'] = 'Nueva Cita'
        data['empresa'] = empresa
        data['form'] = self.form_class()
        data['form2'] = self.second_form_class()
        data['formp'] = UserForm_cliente()
        data['detalle'] = []
        return data


class CrudViewOnline(TemplateView):
    model = Venta
    form_class = VentaForm
    template_name = 'front-end/venta/form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'reserva':
                datos = json.loads(request.POST['ventas'])
                if datos:
                    with transaction.atomic():
                        c = self.model()
                        c.fecha_factura = datos['fecha_venta']
                        c.fecha_reserva = datos['fecha_reserva']
                        c.user_id = datos['cliente']
                        c.duracion_servicio = datos['duracion']
                        c.subtotal = float(datos['subtotal'])
                        c.iva = float(datos['iva'])
                        c.total = float(datos['total'])
                        c.save()
                        if datos['productos']:
                            for i in datos['productos']:
                                dv = Detalle_venta()
                                dv.venta_id = c.id
                                dv.det_compra = int(i['id'])
                                dv.cantidad = int(i['cantidad'])
                                dv.pvp = float(i['pvp'])
                                dv.subtotal = float(i['subtotal'])
                                dv.save()
                        data['id'] = c.id
                        data['resp'] = True
                else:
                    data['resp'] = False
                    data['error'] = "Datos Incompletos"
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Venta'
        data['titulo'] = 'Nueva Venta'
        data['nuevo'] = '/venta/nuevo'
        data['empresa'] = empresa
        data['form'] = self.form_class()
        data['detalle'] = []
        data['formc'] = UserForm()
        return data


def CrudView_online(request):
    data = {}
    if request.user.is_authenticated:
        if request.method == 'GET':
            data['icono'] = opc_icono
            data['entidad'] = 'Compras'
            data['boton'] = 'Pagar'
            data['titulo'] = 'Pagar Compra'
            data['nuevo'] = '/'
            data['empresa'] = empresa
            data['form'] = TransaccionForm()
            data['form2'] = Detalle_VentaForm()
            data['detalle'] = []
            user = Cliente.objects.get(cedula=request.user.cedula)
            data['user'] = user
            return render(request, 'front-end/venta/venta_online.html', data)
    else:
        data['key'] = 1
        data['titulo'] = 'Inicio de Sesion'
        data['nomb'] = nombre_empresa()
        return render(request, 'front-end/login.html', data)


class printpdf(View):
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
            data = []
            result = Detalle_venta.objects.values('det_compra__producto_id', 'pvp', 'subtotal'). \
                filter(venta_id=self.kwargs['pk'], venta__estado=1).annotate(cantidad=Sum('cantidad')).order_by(
                'cantidad')
            result2 = Detalle_servicios.objects.filter(venta_id=self.kwargs['pk'])
            for p1 in result:
                p = Producto.objects.get(id=p1['det_compra__producto_id'])
                data.append({
                    'nombre': p.nombre,
                    'tipo': 'Producto',
                    'duracion': 'N/A',
                    'categoria': p.categoria.nombre,
                    'presentacion': p.presentacion.nombre,
                    'cantidad': p1['cantidad'],
                    'precio': p1['pvp'],
                    'subtotal': p1['subtotal'],
                })
            for s in result2:
                data.append({
                    'nombre': s.servicio.nombre,
                    'tipo': 'Servicio',
                    'duracion': s.servicio.duracion,
                    'categoria': s.servicio.categoria.nombre,
                    'presentacion': 'N/A',
                    'cantidad': s.cantidad,
                    'precio': s.valor,
                    'subtotal': s.subtotals,
                })
        except:
            pass
        return data

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/pdf.html')
            context = {'title': 'Comprobante de Venta',
                       'sale': Venta.objects.get(pk=self.kwargs['pk']),
                       'empresa': Empresa.objects.first(),
                       'det_sale': self.pvp_cal(),
                       'icon': 'media/imagen.png'
                       }
            print(self.pvp_cal())
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('venta:lista'))


class printQR(View):
    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        print(uri)
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

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('front-end/report/lista_qr.html')
            context = {'title': 'Lista de productos con codigo QR',
                       'empresa': Empresa.objects.first(),
                       'producto': Producto.objects.all().prefetch_related()
                       }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Lista_de_QR.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response, link_callback=self.link_callback)
            return response
        except Exception as e:
            pass
        return HttpResponseRedirect(reverse_lazy('producto:lista'))


@csrf_exempt
def grap(request):
    data = {}
    try:
        action = request.POST['action']
        if action == 'chart':
            data = {
                'year': datetime.now().year,
                'ventas': grap_data(),
                'carrusel': grap_imagenes(),
                'tarjets': {
                    'data': data_tarjets()
                }
            }
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


def grap_data():
    year = datetime.now().year
    data = []
    for y in range(1, 13):
        total = Venta.objects.filter(fecha_factura__year=year, fecha_factura__month=y,
                                     estado=1).aggregate(r=Coalesce(Sum('total'), 0)).get('r')
        data.append(float(total))
    return data


def grap_imagenes():
    data = []
    imagenes = Servicio.objects.all()
    for i in imagenes:
        if i.imagen:
            print(i)
            data.append(i.toJSON())
    return data


def data_tarjets():
    data = {}
    try:
        week_start = datetime.now().today()
        week_start -= timedelta(days=week_start.weekday())
        week_end = week_start + timedelta(days=7)
        citas_dia = Venta.objects.filter(fecha_reserva=datetime.now(), estado=2).count()
        citas_semana_hoy = Venta.objects.filter(fecha_reserva__gte=week_start, fecha_reserva__lt=week_end,
                                                estado=2).count()
        total_empleados = Empleado.objects.filter(estado=0).count()
        recaudacion_dia = Venta.objects.values('total').filter(fecha_reserva=datetime.now(), estado=1).aggregate(
            r=Coalesce(Sum('total'), 0)).get('r')
        recaudacion_semana = Venta.objects.values('total').filter(fecha_reserva__range=[week_start, week_end],
                                                                  estado=1).aggregate(r=Coalesce(Sum('total'), 0)).get(
            'r')
        citas_not = Venta.objects.filter(fecha_reserva__gte=week_start, fecha_reserva__lt=datetime.now(),
                                         estado=2).count()
        data = {
            'citas_dia': int(citas_dia),
            'citas_semana_hoy': int(citas_semana_hoy),
            'total_empleados': int(total_empleados),
            'recaudacion_dia': format(float(recaudacion_dia), '.2f'),
            'recaudacion_semana': format(float(recaudacion_semana), '.2f'),
            'citas_not': int(citas_not),
        }
    except Exception as e:
        print(e)
    return data


def dataChart2():
    year = datetime.now().year
    month = datetime.now().month
    data = []
    producto = Producto.objects.all()
    for p in producto:
        total = Detalle_venta.objects.filter(venta__transaccion__fecha_trans__year=year,
                                             venta__transaccion__fecha_trans__month=month,
                                             inventario__produccion__producto_id=p).aggregate(
            r=Coalesce(Sum('venta__transaccion__total'), 0)).get('r')
        data.append({
            'name': p.producto_base.nombre,
            'y': float(total)
        })

    return data


def datachartcontr():
    year = datetime.now().year
    data = []
    for y in range(1, 13):
        totalc = Compra.objects.filter(fecha_compra__year=year, fecha_compra__month=y, estado=1).aggregate(
            r=Coalesce(Sum('total'), 0)).get('r')
        data.append(float(totalc))
    return data


class report(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/report_product.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            empresa = Empresa.objects.first()
            iva = float(empresa.iva / 100)
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Detalle_venta.objects.values('venta__fecha_factura', 'det_compra__producto_id', 'pvp') \
                        .annotate(
                        Sum('cantidad')).filter(venta__estado=1)
                else:
                    query = Detalle_venta.objects.values('venta__fecha_factura', 'det_compra__producto_id', 'pvp') \
                        .filter(venta__fecha_factura__range=[start_date, end_date],
                                venta__estado=1).order_by().annotate(Sum('cantidad'))
                for p in query:
                    total = p['pvp'] * p['cantidad__sum']
                    pr = Producto.objects.get(id=int(p['det_compra__producto_id']))
                    data.append([
                        p['venta__fecha_factura'].strftime("%d/%m/%Y"),
                        pr.nombre,
                        pr.categoria.nombre,
                        pr.presentacion.nombre,
                        int(p['cantidad__sum']),
                        format(p['pvp'], '.2f'),
                        format(total, '.2f'),
                        format((float(total) * iva), '.2f'),
                        format(((float(total) * iva) + float(total)), '.2f')
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Ventas por productos'
        data['empresa'] = empresa
        data['filter_prod'] = '/transaccion/venta/lista'
        return data


class report_servicios(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/report_services.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            empresa = Empresa.objects.first()
            iva = float(empresa.iva / 100)
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Detalle_servicios.objects.values('venta__fecha_factura', 'servicio_id', 'valor') \
                        .annotate(Sum('cantidad')).filter(venta__estado=1)
                else:
                    query = Detalle_servicios.objects.values('venta__fecha_factura', 'servicio_id', 'valor') \
                        .filter(venta__fecha_factura__range=[start_date, end_date], venta__estado=1). \
                        annotate(Sum('cantidad'))
                for p in query:
                    total = p['valor'] * p['cantidad__sum']
                    pr = Servicio.objects.get(id=int(p['servicio_id']))
                    data.append([
                        p['venta__fecha_factura'].strftime("%d/%m/%Y"),
                        pr.nombre,
                        pr.categoria.nombre,
                        pr.duracion,
                        int(p['cantidad__sum']),
                        format(p['valor'], '.2f'),
                        format(total, '.2f'),
                        format((float(total) * iva), '.2f'),
                        format(((float(total) * iva) + float(total)), '.2f')
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de ventas por servicios'
        data['empresa'] = empresa
        data['filter_prod'] = '/transaccion/venta/lista'
        return data


class report_venta_empleado(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/report_venta_empleado.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            empresa = Empresa.objects.first()
            iva = float(empresa.iva / 100)
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Venta.objects.values('empleado_id', 'fecha_factura', 'user_id').annotate(Count('id')).annotate(Sum('subtotal')).annotate(Sum('iva')).annotate(Sum('total')).filter(estado=1)
                else:
                    query = Venta.objects.values('empleado_id', 'fecha_factura', 'user_id').annotate(Count('id')).annotate(Sum('subtotal')).annotate(Sum('iva')).annotate(Sum('total')).filter(fecha_factura__range=[start_date, end_date], estado=1)
                for p in query:
                    emp = Empleado.objects.get(id=int(p['empleado_id'])) if p['empleado_id'] else Empleado.objects.first()
                    cli = User.objects.get(id=int(p['user_id']))
                    data.append([
                        p['fecha_factura'].strftime("%d/%m/%Y"),
                        emp.get_full_name(),
                        cli.get_full_name(),
                        int(p['id__count']),
                        format(p['subtotal__sum'], '.2f'),
                        format(p['iva__sum'], '.2f'),
                        format(p['total__sum'], '.2f')
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion' + str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de ventas por empleado'
        data['empresa'] = empresa
        data['filter_prod'] = '/transaccion/venta/lista'
        return data


class report_total(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/report_total.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Venta.objects.values('fecha_factura', 'user__first_name',
                                                 'user__last_name') \
                        .annotate(Sum('subtotal')).annotate(Sum('iva')).annotate(Sum('total')).filter(estado=1)
                else:
                    query = Venta.objects.values('fecha_factura', 'user__first_name',
                                                 'user__last_name').filter(
                        fecha_factura__range=[start_date, end_date], estado=1). \
                        annotate(Sum('subtotal')).annotate(Sum('iva')).annotate(Sum('total'))
                for p in query:
                    data.append([
                        p['fecha_factura'].strftime("%d/%m/%Y"),
                        p['user__first_name'] + " " + p['user__last_name'],
                        format(p['subtotal__sum'], '.2f'),
                        format((p['iva__sum']), '.2f'),
                        format(p['total__sum'], '.2f')
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Total en Ventas'
        data['titulo'] = 'Reporte de Ventas'
        data['empresa'] = empresa
        data['filter_prod'] = '/transaccion/venta/lista'
        return data


class report_total_reserva(ValidatePermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'front-end/venta/venta_report_total_reserva.html'
    permission_required = 'venta.view_venta'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Venta.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        try:

            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            action = request.POST['action']
            if action == 'report':
                data = []
                if start_date == '' and end_date == '':
                    query = Venta.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos', 'transaccion__user__username') \
                        .annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total')).filter(estado=2)
                else:
                    query = Venta.objects.values('transaccion__fecha_trans', 'transaccion__cliente__nombres',
                                                 'transaccion__cliente__apellidos',
                                                 'transaccion__user__username').filter(
                        transaccion__fecha_trans__range=[start_date, end_date], estado=2). \
                        annotate(Sum('transaccion__subtotal')). \
                        annotate(Sum('transaccion__iva')).annotate(Sum('transaccion__total'))
                for p in query:
                    data.append([
                        p['transaccion__fecha_trans'].strftime("%d/%m/%Y"),
                        p['transaccion__cliente__nombres'] + " " + p['transaccion__cliente__apellidos'],
                        p['transaccion__user__username'],
                        format(p['transaccion__subtotal__sum'], '.2f'),
                        format((p['transaccion__iva__sum']), '.2f'),
                        format(p['transaccion__total__sum'], '.2f')
                    ])
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Ventas Reservadas'
        data['titulo'] = 'Reporte de Pedidos'
        data['empresa'] = empresa
        return data
