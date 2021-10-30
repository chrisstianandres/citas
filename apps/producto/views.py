import json
from io import BytesIO

import qrcode
import rsa

from datetime import datetime

from PIL import Image, ImageDraw
from django.core.files import File
from django.db.models import Q, Sum, Count
from django.db.models.functions import Coalesce

from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from apps.backEnd import nombre_empresa, PrimaryKeyEncryptor
from apps.categoria.forms import CategoriaForm
from apps.compra.models import Detalle_compra
from apps.empresa.models import Empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.presentacion.forms import PresentacionForm
from apps.producto.forms import ProductoForm
from apps.producto.models import Producto

from apps.venta.models import Detalle_venta
from citas.settings import SECRET_KEY_ENCRIPT

opc_icono = 'fab fa-amazon'
opc_entidad = 'Productos'
crud = '/producto/nuevo'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'front-end/producto/list.html'
    permission_required = 'producto.view_producto'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in self.model.objects.all():
                    data.append(c.toJSON())
            elif action == 'list_list':
                data = []
                ids = json.loads(request.POST['ids'])
                query = self.model.objects.all()
                for c in query.exclude(id__in=ids):
                    item = c.toJSON()
                    item['precio'] = 0.50
                    item['cantidad'] = 1
                    item['subtotal'] = 0.00
                    data.append(item)
            elif action == 'delete':
                pk = request.POST['id']
                f = self.model.objects.get(pk=pk)
                f.delete()
            # elif action == 'list_venta':
            #     data = []
            #     vent = Producto.objects.filter(stock__gte=1)
            #     ids = json.loads(request.POST['ids'])
            #     for c in vent.exclude(producto_base_id__in=ids):
            #         data.append(c.toJSON())
            # elif action == 'search':
            #     data = []
            #     term = request.POST['term']
            #     ids = json.loads(request.POST['ids'])
            #     query = Producto.objects.filter(producto_base__nombre__icontains=term, stock__gte=1)
            #     for a in query.exclude(producto_base_id__in=ids)[0:10]:
            #         result = {'id': int(a.id), 'text': str(a.producto_base.nombre)}
            #         data.append(result)
            # elif action == 'search_rep':
            #     data = []
            #     ids = json.loads(request.POST['ids'])
            #     term = request.POST['term']
            #     query = Producto.objects.filter(
            #         Q(producto_base__nombre__icontains=term) | Q(producto_base__color__nombre__icontains=term))
            #     for a in query.exclude(producto_base_id__in=ids)[0:10]:
            #         result = {'id': int(a.id),
            #                   'text': str(str(a.producto_base.nombre) + ' / ' + str(a.producto_base.color.nombre))}
            #         data.append(result)
            # elif action == 'get':
            #     data = []
            #     id = request.POST['id']
            #     producto = Producto.objects.filter(pk=id)
            #     empresa = Empresa.objects.first()
            #     for i in producto:
            #         item = i.toJSON()
            #         item['cantidad'] = 1
            #         item['subtotal'] = 0.00
            #         item['iva_emp'] = empresa.iva
            #         data.append(item)
            # elif action == 'get_rep':
            #     data = []
            #     id = request.POST['id']
            #     producto = Producto.objects.filter(pk=id)
            #     empresa = Empresa.objects.first()
            #     for i in producto:
            #         item = i.toJSON()
            #         item['cantidad'] = 1
            #         item['pvp'] = 1.00
            #         item['subtotal'] = 0.00
            #         item['iva_emp'] = empresa.iva
            #         data.append(item)
            # elif action == 'get_confec':
            #     data = []
            #     id = request.POST['id']
            #     producto = Producto.objects.filter(pk=id)
            #     empresa = Empresa.objects.first()
            #     for i in producto:
            #         item = i.toJSON()
            #         item['cantidad'] = 1
            #         item['pvp'] = format(i.pvp_confec, '.2f')
            #         item['subtotal'] = 0.00
            #         item['iva_emp'] = empresa.iva
            #         data.append(item)
            # elif action == 'sitio':
            #     data = []
            #     h = datetime.today()
            #     query = Detalle_venta.objects.filter(venta__transaccion__fecha_trans__month=h.month,
            #                                          venta__estado=1).values('inventario__producto__producto_base_id',
            #                                                                  'inventario__producto_id',
            #                                                                  'inventario__producto__pvp',
            #                                                                  'inventario__producto__pvp_alq',
            #                                                                  'inventario__producto__pvp_confec',
            #                                                                  'inventario__producto__imagen').annotate(
            #         total=Sum('cantidad')).order_by('-total')[0:3]
            #     for i in query:
            #         px = Producto_base.objects.get(id=int(i['inventario__producto__producto_base_id']))
            #         pr = Producto.objects.get(id=int(i['inventario__producto_id']))
            #         item = {'info': px.nombre, 'descripcion': px.descripcion}
            #         item['id_venta'] = int(i['inventario__producto_id'])
            #         item['id_reparacion'] = int(pr.id)
            #         item['id_confeccion'] = int(pr.id)
            #         item['pvp'] = format(i['inventario__producto__pvp'], '.2f')
            #         item['pvp_alq'] = format(i['inventario__producto__pvp_alq'], '.2f')
            #         item['pvp_confec'] = format(i['inventario__producto__pvp_confec'], '.2f')
            #         item['imagen'] = pr.get_image()
            #         data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Producto'
        data['titulo'] = 'Listado de Productos'
        data['nuevo'] = '/producto/nuevo'
        data['empresa'] = empresa
        return data


class report(ValidatePermissionRequiredMixin, ListView):
    model = Producto
    template_name = 'front-end/producto/report.html'
    permission_required = 'producto.view_producto'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'report':
                data = []
                for c in Producto.objects.all():
                    data.append(c.toJSON())
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Producto'
        data['titulo'] = 'Listado de Productos'
        data['nuevo'] = '/producto/nuevo'
        data['empresa'] = empresa
        return data


class inventario(ValidatePermissionRequiredMixin, ListView):
    model = Producto
    seccond_model = Detalle_compra
    template_name = 'front-end/producto/inventario.html'
    permission_required = 'producto.view_producto'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in self.model.objects.all():
                    stock = self.seccond_model.objects.filter(compra__estado=1, producto_id=c.id).aggregate(
                        stock=Coalesce(Sum('stock_actual'), 0)).get('stock')
                    item = c.toJSON()
                    item['stock'] = stock
                    data.append(item)
            elif action == 'list_list':
                data = []
                ids = json.loads(request.POST['ids'])
                query = self.model.objects.all()
                for c in query.exclude(id__in=ids):
                    item = c.toJSON()
                    item['precio'] = 0.50
                    item['cantidad'] = 1
                    item['subtotal'] = 0.00
                    data.append(item)
            # elif action == 'list_venta':
            #     data = []
            #     vent = Producto.objects.filter(stock__gte=1)
            #     ids = json.loads(request.POST['ids'])
            #     for c in vent.exclude(producto_base_id__in=ids):
            #         data.append(c.toJSON())
            # elif action == 'search':
            #     data = []
            #     term = request.POST['term']
            #     ids = json.loads(request.POST['ids'])
            #     query = Producto.objects.filter(producto_base__nombre__icontains=term, stock__gte=1)
            #     for a in query.exclude(producto_base_id__in=ids)[0:10]:
            #         result = {'id': int(a.id), 'text': str(a.producto_base.nombre)}
            #         data.append(result)
            # elif action == 'search_rep':
            #     data = []
            #     ids = json.loads(request.POST['ids'])
            #     term = request.POST['term']
            #     query = Producto.objects.filter(
            #         Q(producto_base__nombre__icontains=term) | Q(producto_base__color__nombre__icontains=term))
            #     for a in query.exclude(producto_base_id__in=ids)[0:10]:
            #         result = {'id': int(a.id),
            #                   'text': str(str(a.producto_base.nombre) + ' / ' + str(a.producto_base.color.nombre))}
            #         data.append(result)
            # elif action == 'get':
            #     data = []
            #     id = request.POST['id']
            #     producto = Producto.objects.filter(pk=id)
            #     empresa = Empresa.objects.first()
            #     for i in producto:
            #         item = i.toJSON()
            #         item['cantidad'] = 1
            #         item['subtotal'] = 0.00
            #         item['iva_emp'] = empresa.iva
            #         data.append(item)
            # elif action == 'get_rep':
            #     data = []
            #     id = request.POST['id']
            #     producto = Producto.objects.filter(pk=id)
            #     empresa = Empresa.objects.first()
            #     for i in producto:
            #         item = i.toJSON()
            #         item['cantidad'] = 1
            #         item['pvp'] = 1.00
            #         item['subtotal'] = 0.00
            #         item['iva_emp'] = empresa.iva
            #         data.append(item)
            # elif action == 'get_confec':
            #     data = []
            #     id = request.POST['id']
            #     producto = Producto.objects.filter(pk=id)
            #     empresa = Empresa.objects.first()
            #     for i in producto:
            #         item = i.toJSON()
            #         item['cantidad'] = 1
            #         item['pvp'] = format(i.pvp_confec, '.2f')
            #         item['subtotal'] = 0.00
            #         item['iva_emp'] = empresa.iva
            #         data.append(item)
            # elif action == 'sitio':
            #     data = []
            #     h = datetime.today()
            #     query = Detalle_venta.objects.filter(venta__transaccion__fecha_trans__month=h.month,
            #                                          venta__estado=1).values('inventario__producto__producto_base_id',
            #                                                                  'inventario__producto_id',
            #                                                                  'inventario__producto__pvp',
            #                                                                  'inventario__producto__pvp_alq',
            #                                                                  'inventario__producto__pvp_confec',
            #                                                                  'inventario__producto__imagen').annotate(
            #         total=Sum('cantidad')).order_by('-total')[0:3]
            #     for i in query:
            #         px = Producto_base.objects.get(id=int(i['inventario__producto__producto_base_id']))
            #         pr = Producto.objects.get(id=int(i['inventario__producto_id']))
            #         item = {'info': px.nombre, 'descripcion': px.descripcion}
            #         item['id_venta'] = int(i['inventario__producto_id'])
            #         item['id_reparacion'] = int(pr.id)
            #         item['id_confeccion'] = int(pr.id)
            #         item['pvp'] = format(i['inventario__producto__pvp'], '.2f')
            #         item['pvp_alq'] = format(i['inventario__producto__pvp_alq'], '.2f')
            #         item['pvp_confec'] = format(i['inventario__producto__pvp_confec'], '.2f')
            #         item['imagen'] = pr.get_image()
            #         data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Stock de Productos'
        data['empresa'] = empresa
        return data


class Createview(ValidatePermissionRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    success_url = 'producto:lista'
    template_name = 'front-end/producto/form.html'
    permission_required = 'producto.add_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                from apps.backEnd import PrimaryKeyEncryptor
                f = self.form_class(request.POST or None, request.FILES or None)
                if f.is_valid():
                    var = f.save()
                    if var.pk:
                        encr = PrimaryKeyEncryptor(SECRET_KEY_ENCRIPT).encrypt(var.pk)
                        string = 'http://monicagarces.pythonanywhere.com/producto/detalle/' + str(encr)
                        qrcode_code = qrcode.make(str(string))
                        canvas = Image.new('RGB', (500, 500), 'white')
                        draw = ImageDraw.Draw(canvas)
                        canvas.paste(qrcode_code)
                        fname = f'qr-code{var.nombre}' + '.png'
                        buffer = BytesIO()
                        canvas.save(buffer, 'png')
                        var.qr.save(fname, File(buffer), save=False)
                        canvas.close()
                        var.save()
                    data['producto'] = var.toJSON()
                    data['resp'] = True
                else:
                    data['error'] = f.errors
                    data['form'] = f
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = self.model.objects.filter(nombre__icontains=term)[0:10]
                for a in query:
                    result = {'id': int(a.id),
                              'text': 'Nombre: ' + str(a.nombre) + ' / ' + 'Descripcion: ' + str(a.descripcion)}
                    data.append(result)
            elif action == 'get':
                data = []
                pk = request.POST['id']
                query = self.model.objects.get(id=pk)
                item = query.toJSON()
                data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            var = f.save()
            data['producto'] = var.toJSON()
            data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if 'form' not in data:
            data['form'] = self.form_class(self.request.GET)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Producto'
        data['titulo'] = 'Nuevo Registro de un Producto'
        data['nuevo'] = '/producto/nuevo'
        data['action'] = 'add'
        data['crud'] = crud
        data['form_cat'] = CategoriaForm
        data['form_pres'] = PresentacionForm
        data['form_prod'] = ProductoForm
        data['empresa'] = empresa
        return data


class Updateview(ValidatePermissionRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    success_url = 'producto:lista'
    template_name = 'front-end/producto/form.html'
    permission_required = 'producto.change_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            pk = self.kwargs.get('pk', 0)
            producto = self.model.objects.get(id=pk)
            if action == 'edit':
                f = self.form_class(request.POST or None, request.FILES or None, instance=producto)
                if f.is_valid():
                    var = f.save()
                    data['producto'] = var.toJSON()
                    data['resp'] = True
                else:
                    data['error'] = f.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        producto = self.model.objects.get(id=pk)
        if 'form' not in data:
            data['form'] = self.form_class(instance=producto)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Edicion del Registro de un Producto'
        data['action'] = 'edit'
        data['crud'] = '/producto/editar/' + str(self.kwargs['pk'])
        data['form_cat'] = CategoriaForm
        data['form_pres'] = PresentacionForm
        data['empresa'] = empresa
        return data


@csrf_exempt
def index(request):
    data = {}
    try:
        data = []
        for p in Producto.objects.filter(stock__range=[1, 10]):
            data.append(p.toJSON())
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


@csrf_exempt
def get_prod(request):
    data = {}
    try:
        data = []
        id = request.POST['id']
        producto = Producto.objects.filter(pk=id)
        empresa = Empresa.objects.first()
        for i in producto:
            item = i.toJSON()
            item['cantidad'] = 1
            item['subtotal'] = 0.00
            item['iva_emp'] = empresa.iva
            data.append(item)
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data, safe=False)


def detalle_producto_qr(request, pk):
    data = {}
    try:
        detalle = []
        desencr = PrimaryKeyEncryptor(SECRET_KEY_ENCRIPT).decrypt(pk)
        producto = Producto.objects.get(id=int(desencr))
        prod = Detalle_compra.objects.filter(compra__estado=1, producto_id=producto.id)
        stock = prod.prefetch_related('producto').aggregate(stock=Coalesce(Sum('stock_actual'), 0)).get('stock')
        pvp = prod.annotate(pvp=Count('precio_venta'))
        item = producto.toJSON()
        item['stock'] = stock
        detalle.append(item)
        data = {'empresa': empresa, 'producto': producto, 'stock': stock, 'pvp': pvp.first().precio_venta if pvp else 0.00}
    except Exception as e:
        print(e)
    return render(request, 'front-end/producto/detalle_producto_qr.html', data)

