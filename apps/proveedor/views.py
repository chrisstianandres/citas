import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, UpdateView, DeleteView

from apps.backEnd import nombre_empresa, verificar
from apps.mixins import ValidatePermissionRequiredMixin
from apps.user.models import User
from apps.proveedor.forms import ProveedorForm
from apps.proveedor.models import Proveedor

opc_icono = 'fa fa-user-circle'
opc_entidad = 'Proveedor'
crud = '/proveedor/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Proveedor
    template_name = "front-end/proveedor/list.html"
    permission_required = 'proveedor.view_proveedor'

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
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = self.model.objects.filter(
                    Q(nombres__icontains=term) | Q(apellidos__icontains=term) | Q(num_doc=term))[0:10]
                for a in query:
                    item = a.toJSON()
                    item['text'] = a.get_full_name()
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado una opcion'
            import json
        except Exception as e:
            data['error'] = str(e)
            print(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar'
        data['titulo'] = 'Proveedores'
        data['titulo_lista'] = 'Listado de Proveedores'
        data['titulo_formulario'] = 'Formulario de Registro'
        data['nuevo'] = '/proveedor/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = ProveedorForm
    model = Proveedor
    template_name = 'front-end/proveedor/form.html'
    permission_required = 'proveedor.add_proveedor'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = self.form_class(request.POST)
                data = self.save_data(f)
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = self.model.objects.filter(nombre__icontains=term)
                for a in query[0:10]:
                    result = {'id': int(a.id), 'text': str(a.nombre)}
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
            f.save(commit=False)
            if int(f.data['tipo']) == 0:
                if verificar(f.data['num_doc']):
                    prod = f.save()
                    data['resp'] = True
                    data['proveedor'] = prod.toJSON()
                else:
                    f.add_error("num_doc", "Numero de Cedula no valido para Ecuador")
                    data['error'] = f.errors
            else:
                if verificar(f.data['num_doc']):
                    prod = f.save()
                    data['resp'] = True
                    data['proveedor'] = prod.toJSON()
                else:
                    f.add_error("num_doc", "Numero de Ruc no valido para Ecuador")
                    data['error'] = f.errors
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Nuevo Proveedor'
        data['nuevo'] = '/proveedor/nuevo'
        data['action'] = 'add'
        data['empresa'] = empresa
        data['form'] = self.form_class
        return data


class ActualizarView(ValidatePermissionRequiredMixin, UpdateView):
    form_class = ProveedorForm
    model = Proveedor
    template_name = 'front-end/proveedor/form.html'
    permission_required = 'proveedor.change_proveedor'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                pk = self.kwargs['pk']
                cat = self.model.objects.get(pk=int(pk))
                f = self.form_class(request.POST, instance=cat)
                data = self.save_data(f)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            f.save(commit=False)
            if int(f.data['tipo']) == 0:
                if verificar(f.data['num_doc']):
                    prod = f.save()
                    data['resp'] = True
                    data['proveedor'] = prod.toJSON()
                else:
                    f.add_error("num_doc", "Numero de Cedula no valido para Ecuador")
                    data['error'] = f.errors
            else:
                if verificar(f.data['num_doc']):
                    prod = f.save()
                    data['resp'] = True
                    data['proveedor'] = prod.toJSON()
                else:
                    f.add_error("num_doc", "Numero de Ruc no valido para Ecuador")
                    data['error'] = f.errors
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Editar una Empleado'
        data['action'] = 'edit'
        data['empresa'] = empresa
        dato = self.model.objects.get(pk=self.kwargs['pk'])
        data['form'] = self.form_class(instance=dato)
        return data


class EliminarView(ValidatePermissionRequiredMixin, DeleteView):
    model = Proveedor
    permission_required = 'proveedor.delete_proveedor'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            pk = request.POST['id']
            cat = self.model.objects.get(pk=pk)
            cat.delete()
            data['resp'] = True
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')


class report(ValidatePermissionRequiredMixin, ListView):
    model = Proveedor
    template_name = 'front-end/proveedor/report.html'
    permission_required = 'proveedor.view_proveedor'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.none()

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        if action == 'report':
            data = []
            start_date = request.POST.get('start_date', '')
            end_date = request.POST.get('end_date', '')
            try:
                if start_date == '' and end_date == '':
                    query = self.model.objects.all()
                else:
                    query = self.model.objects.filter(fecha__range=[start_date, end_date])

                for p in query:
                    data.append(p.toJSON())
            except:
                pass
            return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Reporte de Proveedores'
        data['titulo'] = 'Reporte de Proveedores'
        data['empresa'] = empresa
        return data
