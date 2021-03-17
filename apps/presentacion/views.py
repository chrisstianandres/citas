import json

from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.presentacion.forms import PresentacionForm
from apps.presentacion.models import Presentacion

opc_icono = 'fas fa-box-open'
opc_entidad = 'Presentacion'
crud = '/presentacion/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Presentacion
    template_name = 'front-end/presentacion/list.html'
    permission_required = 'presentacion.view_presentacion'

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
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nueva Presentacion'
        data['titulo'] = 'Listado de Presentaciones'
        data['nuevo'] = '/presentacion/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = PresentacionForm
    model = Presentacion
    template_name = 'front-end/presentacion/form.html'
    permission_required = 'presentacion.add_presentacion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        print(request.POST['action'])
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
            if self.model.objects.filter(nombre__icontains=f.data['nombre']):
                f.add_error("nombre", "Ya existe una Presentacion este nombre")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['presentacion'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def edit_data(self, f, pk):
        data = {}
        if f.is_valid():
            f.save(commit=False)
            if self.model.objects.filter(nombre__icontains=f.data['nombre']).exclude(pk=pk):
                f.add_error("nombre", "Ya existe una Presentacion este nombre")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['Presentacion'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Nueva Presentacion'
        data['nuevo'] = '/presentacion/nuevo'
        data['action'] = 'add'
        data['empresa'] = empresa
        data['form'] = self.form_class
        return data


class UpdateView(ValidatePermissionRequiredMixin, UpdateView):
    form_class = PresentacionForm
    model = Presentacion
    template_name = 'front-end/presentacion/form.html'
    permission_required = 'presentacion.change_presentacion'

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
                data = self.edit_data(f, pk)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def save_data(self, f):
        data = {}
        if f.is_valid():
            f.save(commit=False)
            if self.model.objects.filter(nombre__icontains=f.data['nombre']):
                f.add_error("nombre", "Ya existe una Presentacion este nombre")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['presentacion'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def edit_data(self, f, pk):
        data = {}
        if f.is_valid():
            f.save(commit=False)
            if self.model.objects.filter(nombre__icontains=f.data['nombre']).exclude(pk=pk):
                f.add_error("nombre", "Ya existe una Presentacion este nombre")
                data['error'] = f.errors
            else:
                var = f.save()
                data['resp'] = True
                data['presentacion'] = var.toJSON()
                data['resp'] = True
        else:
            data['error'] = f.errors
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Editar una Presentacion'
        data['action'] = 'edit'
        data['empresa'] = empresa
        dato = self.model.objects.get(pk=self.kwargs['pk'])
        data['form'] = self.form_class(instance=dato)
        return data


class DeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Presentacion
    permission_required = 'presentacion.delete_presentacion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'delete':
                pk = request.POST['id']
                cat = self.model.objects.get(pk=pk)
                cat.delete()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')


