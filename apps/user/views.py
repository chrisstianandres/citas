import json

from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, request
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, TemplateView

from apps.backEnd import nombre_empresa
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.forms import GroupForm
from apps.user.forms import UserForm, UserForm_online, UserForm_cliente
from apps.user.models import User
from apps.proveedor.models import Proveedor

opc_icono = 'fas fa-user-shield'
opc_entidad = 'Usuarios'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'front-end/cliente/list.html'
    permission_required = 'user.view_user'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                user = User.objects.filter(tipo=0)
                for c in user:
                    data.append(c.toJSON())
            elif action == 'estado':
                id = request.POST['id']
                ps = User.objects.get(pk=id)
                if ps.estado == 1:
                    ps.estado = 0
                    ps.save()
                    data['resp'] = True
                elif ps.estado == 0:
                    ps.estado = 1
                    ps.save()
                    data['resp'] = True
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'delete':
                id = request.POST['id']
                if id:
                    ps = User.objects.get(pk=id)
                    ps.delete()
                    data['resp'] = True
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Cliente'
        data['titulo'] = 'Listado de Clientes'
        data['nuevo'] = '/persona/cliente/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = UserForm_cliente
    template_name = 'front-end/cliente/form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = self.form_class(request.POST, request.FILES)
                if f.is_valid():
                    f.save()
                else:
                    data['errior'] = f.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Cliente'
        data['titulo'] = 'Registro de Clientes'
        data['form'] = self.form_class
        data['action'] = 'add'
        data['empresa'] = empresa
        return data


class Updateview(ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm_cliente
    template_name = 'front-end/cliente/form.html'
    permission_required = 'user.change_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            pk = self.kwargs.get('pk', 0)
            user = self.model.objects.get(id=pk)
            if action == 'edit':
                f = self.form_class(request.POST, request.FILES, instance=user)
                f.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        user = self.model.objects.get(id=pk)
        data['form'] = self.form_class(instance=user)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Edicion del Registro de un Cliente'
        data['action'] = 'edit'
        dato = self.model.objects.get(pk=self.kwargs['pk'])
        data['form'] = self.form_class(instance=dato)
        data['empresa'] = empresa
        return data


class Listgroupsview(ValidatePermissionRequiredMixin, ListView):
    model = Group
    template_name = 'front-end/group/group_list.html'
    permission_required = 'user.view_user'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                user = Group.objects.all()
                for c in user:
                    data.append({'id': int(c.id), 'nombre': str(c.name),
                                 'permisos': [{'id': p.id, 'nombre': p.name} for p in c.permissions.all()]})
                    print(data)
            elif action == 'delete':
                try:
                    id = request.POST['id']
                    if id:
                        ps = User.objects.get(pk=id)
                        ps.delete()
                        data['resp'] = True
                    else:
                        data['error'] = 'Ha ocurrido un error'
                except Exception as e:
                    data['error'] = str(e)
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = 'No ha seleccionado una opcion'
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-user-lock'
        data['entidad'] = 'Grupos'
        data['boton'] = 'Nuevo Grupo'
        data['titulo'] = 'Listado de Grupos'
        data['nuevo'] = '/usuario/grupo'
        data['form'] = UserForm
        data['empresa'] = empresa
        return data


class CrudViewGroup(ValidatePermissionRequiredMixin, TemplateView):
    form_class = Group
    template_name = 'front-end/group/group_form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = GroupForm(request.POST)
                if f.is_valid():
                    f.save()
                    return HttpResponseRedirect('user/groups')
                else:
                    data['form'] = f
                return render(request, 'front-end/group/group_form.html', data)
            elif action == 'delete':
                pk = request.POST['id']
                cli = Group.objects.get(pk=pk)
                cli.delete()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Guardar Grupo'
        data['titulo'] = 'Nuevo Grupos'
        data['nuevo'] = '/usuario/newgroup'
        data['form'] = GroupForm
        data['action'] = 'add'
        data['empresa'] = empresa
        return data


class lista_user(ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'front-end/user/list.html'
    permission_required = 'user.view_user'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'list':
                data = []
                user = User.objects.filter(tipo=1)
                for c in user:
                    data.append(c.toJSON())
            elif action == 'estado':
                id = request.POST['id']
                ps = User.objects.get(pk=id)
                if ps.estado == 1:
                    ps.estado = 0
                    ps.save()
                    data['resp'] = True
                elif ps.estado == 0:
                    ps.estado = 1
                    ps.save()
                    data['resp'] = True
                else:
                    data['error'] = 'Ha ocurrido un error'
            elif action == 'delete':
                id = request.POST['id']
                if id:
                    ps = User.objects.get(pk=id)
                    ps.delete()
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
        data['icono'] = 'fa fa-male'
        data['entidad'] = 'Usuarios'
        data['boton'] = 'Nuevo Usuario'
        data['titulo'] = 'Listado de Usuarios'
        data['nuevo'] = '/persona/usuario/nuevo'
        data['empresa'] = empresa
        return data


class CrudView_user(ValidatePermissionRequiredMixin, TemplateView):
    form_class = UserForm
    template_name = 'front-end/user/form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                f = self.form_class(request.POST, request.FILES)
                if f.is_valid():
                    f.save()
                else:
                    data['errior'] = f.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = 'fa fa-male'
        data['entidad'] = 'Usuarios'
        data['boton'] = 'Nuevo Usuario'
        data['titulo'] = 'Registro de Usuarios'
        data['form'] = self.form_class
        data['action'] = 'add'
        data['empresa'] = empresa
        return data


class Updateview_user(ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'front-end/user/form.html'
    permission_required = 'user.change_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            pk = self.kwargs.get('pk', 0)
            user = self.model.objects.get(id=pk)
            print(request.POST)
            if action == 'edit':
                f = self.form_class(request.POST, request.FILES, instance=user)
                f.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        user = self.model.objects.get(id=pk)
        data['form'] = self.form_class(instance=user)
        data['icono'] = 'fa fa-male'
        data['entidad'] = 'Usuarios'
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Edicion del Registro de un Usuario'
        data['action'] = 'edit'
        dato = self.model.objects.get(pk=self.kwargs['pk'])
        data['form'] = self.form_class(instance=dato)
        data['empresa'] = empresa
        return data
@csrf_exempt
def estado(request):
    data = {}
    try:
        id = int(request.POST['id'])
        ps = User.objects.get(pk=id)
        if ps.estado == 1:
            ps.estado = 0
            ps.save()
            data['resp'] = True
        elif ps.estado == 0:
            ps.estado = 1
            ps.save()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = str(e)
    return JsonResponse(data)


def profile(request):
    empleado = User.objects.get(id=request.user.id)
    crud = '/user/profile'
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud,
        'boton': 'Guardar Uusuario', 'action': 'add', 'titulo': 'Perfil de Usuario', 'empresa': nombre_empresa()
    }
    if request.method == 'GET':
        form = UserForm(instance=empleado)
        data['form'] = form
    else:
        form = UserForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/profile')
        else:
            data['form'] = form
    return render(request, 'front-end/profile.html', data)
    # return render(request, 'front-end/profile.html', data)

