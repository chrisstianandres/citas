import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, TemplateView
from django.views.generic.base import View

from apps.backEnd import nombre_empresa, send_email_contrasena
from apps.mixins import ValidatePermissionRequiredMixin
from apps.producto.forms import GroupForm
from apps.user.forms import UserForm, UserForm_online, UserForm_cliente, UserForm_profile, UserForm_password
from apps.user.models import User
from apps.proveedor.models import Proveedor

opc_icono = 'fas fa-user-shield'
opc_entidad = 'Usuarios'
opc_entidad_cliente = 'Clientes'
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
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad_cliente
        data['boton'] = 'Nuevo Cliente'
        data['titulo'] = 'Listado de Clientes'
        data['nuevo'] = '/persona/cliente/nuevo'
        data['empresa'] = empresa
        return data


class report_cliente(ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'front-end/cliente/report.html'
    permission_required = 'user.view_user'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                data = []
                if start_date == '' and end_date == '':
                    query = self.model.objects.filter(tipo=0)
                else:
                    query = self.model.objects.filter(tipo=0, date_joined__range=[start_date, end_date])
                for p in query:
                    data.append(p.toJSON())
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad_cliente
        data['titulo'] = 'Reporte de Clientes'
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
                    data['error'] = f.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad_cliente
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
                if f.is_valid():
                    f.save()
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
            elif action == 'delete':
                try:
                    id = request.POST['id']
                    if id:
                        ps = Group.objects.get(pk=id)
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
        data['nuevo'] = reverse_lazy('user:newgroup')
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
                with transaction.atomic():
                    datos = json.loads(request.POST['permisos'])
                    grupo = Group()
                    grupo.name = datos['nombre']
                    grupo.save()
                    if datos['detalle']:
                        for p in datos['detalle']:
                            name = '{}_{}'.format(p['tipo'], p['modelo'])
                            permiso = Permission.objects.get(codename=name)
                            grupo.permissions.add(permiso.id)
                    data['resp'] = True
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
        data['permisos'] = ContentType.objects.all().exclude(model__in=['logentry', 'permission', 'session', 'contenttype',
                                                                        'detalle_venta', 'detalle_compra', 'detalle_maquinas',
                                                                        'detalle_servicios', 'detalle_servicios_duracion',
                                                                        'envio_stock_dia', 'devolucion_compra', 'devolucion_venta'])
        return data


class UpdateGroup(ValidatePermissionRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'front-end/group/group_form.html'
    success_url = 'user:groups'
    permission_required = 'auth.add_change'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                datos = json.loads(request.POST['permisos'])
                grupo = Group.objects.get(id=self.kwargs['pk'])
                grupo.permissions.clear()
                grupo.name = datos['nombre']
                grupo.save()
                if datos['detalle']:
                    for p in datos['detalle']:
                        name = '{}_{}'.format(p['tipo'], p['modelo'])
                        permiso = Permission.objects.get(codename=name)
                        grupo.permissions.add(permiso.id)
                data['resp'] = True
            elif action == 'add':
                datos = json.loads(request.POST['permisos'])
                grupo = Group.objects.get(id=self.kwargs['pk'])
                grupo.permissions.clear()
                grupo.name = datos['nombre']
                grupo.save()
                for p in datos['modelos']:
                    if p['check'] == 1:
                        add = '{}_{}'.format('add', p['nombre'])
                        permiso_add = Permission.objects.get(codename=add)
                        grupo.permissions.add(permiso_add.id)
                        view = '{}_{}'.format('view', p['nombre'])
                        permiso_view = Permission.objects.get(codename=view)
                        grupo.permissions.add(permiso_view.id)
                        change = '{}_{}'.format('change', p['nombre'])
                        permiso_change = Permission.objects.get(codename=change)
                        grupo.permissions.add(permiso_change.id)
                        delete = '{}_{}'.format('delete', p['nombre'])
                        permiso_delete = Permission.objects.get(codename=delete)
                        grupo.permissions.add(permiso_delete.id)
                    grupo.save()
                data['resp'] = True
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get(self, request, *args, **kwargs):
        try:
            context = {}
            data = []
            pk = self.kwargs['pk']
            contentype = ContentType.objects.all().order_by('model')
            x = 1
            for c in contentype.exclude(model__in=['logentry', 'permission', 'session', 'contenttype',
                                                   'detalle_venta', 'detalle_compra', 'detalle_maquinas',
                                                   'detalle_servicios', 'detalle_servicios_duracion',
                                                   'envio_stock_dia', 'devolucion_compra', 'devolucion_venta']):
                nombre = c.model
                set_add = 0
                set_delete = 0
                set_edit = 0
                set_view = 0
                permisos_select = []
                if Group.objects.filter(permissions__content_type__model=nombre, id=pk,
                                        permissions__codename='add_' + str(nombre)):
                    set_add = 1
                    permisos_select.append({'tipo': 'add', 'modelo': nombre})
                if Group.objects.filter(permissions__content_type__model=nombre, id=pk,
                                        permissions__codename='change_' + str(nombre)):
                    set_edit = 1
                    permisos_select.append({'tipo': 'edit', 'modelo': nombre})
                if Group.objects.filter(permissions__content_type__model=nombre, id=pk,
                                        permissions__codename='delete_' + str(nombre)):
                    set_delete = 1
                    permisos_select.append({'tipo': 'delete', 'modelo': nombre})
                if Group.objects.filter(permissions__content_type__model=nombre, id=pk,
                                        permissions__codename='view_' + str(nombre)):
                    set_view = 1
                    permisos_select.append({'tipo': 'view', 'modelo': nombre})
                data.append({'model': nombre, 'num': x, 'add': set_add, 'edit': set_edit, 'delete': set_delete,
                             'view': set_view})
                x += 1
            grupo = self.model.objects.get(id=self.kwargs['pk'])
            context['icono'] = opc_icono
            context['entidad'] = 'Grupos'
            context['boton'] = 'Guardar Grupo'
            context['titulo'] = 'Editar Grupos'
            context['nuevo'] = '/usuario/newgroup'
            context['form'] = GroupForm(instance=grupo)
            context['action'] = 'edit'
            context['empresa'] = empresa
            context['option'] = 'editar'
            context['permisos'] = data
            context['permisos_select'] =  permisos_select
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            pass

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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


class report_user(ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'front-end/cliente/report.html'
    permission_required = 'user.view_user'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                data = []
                if start_date == '' and end_date == '':
                    query = self.model.objects.filter(tipo=1)
                else:
                    query = self.model.objects.filter(tipo=1, date_joined__range=[start_date, end_date])
                for p in query:
                    data.append(p.toJSON())
            else:
                data['error'] = 'No ha seleccionado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['titulo'] = 'Reporte de Usuarios'
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


class Profile(ValidatePermissionRequiredMixin, TemplateView):
    model = User
    form_class = UserForm_profile
    seccond_form_class = UserForm_password
    template_name = 'front-end/user/profile.html'
    permission_required = 'user.change_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            user = self.model.objects.get(id=request.user.id)
            if action == 'edit':
                f = self.form_class(request.POST, request.FILES, instance=user)
                f.save()
            elif action == 'password':
                f = PasswordChangeForm(user=request.user, data=request.POST)
                if f.is_valid():
                    f.save()
                    user = User.objects.get(id=request.user.id)
                    user.resetpass = False
                    user.save()
                    update_session_auth_hash(request, f.user)
                else:
                    data['error'] = f.errors
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = 'Perfil de Usuario'
        data['boton'] = 'Guardar Edicion'
        data['titulo'] = 'Perfil de Usuario'
        data['action'] = 'edit'
        dato = self.model.objects.get(pk=self.request.user.id)
        data['form'] = self.form_class(instance=dato)
        data['form_password'] = PasswordChangeForm(user=self.request.user)
        data['empresa'] = empresa
        return data


class UserChangeGroup(View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('menu'))

@csrf_exempt
def ResetPass(request):
    if request.user.is_authenticated:
       context = {'form_password': PasswordChangeForm(request.user), 'empresa': nombre_empresa()}
       return render(request, 'front-end/password_change.html', context)
    else:
        data={}
        cedula = request.POST['cedula']
        if User.objects.filter(cedula=cedula).exists():
            usuario = User.objects.get(cedula=cedula)
            passw = get_random_string(8)
            usuario.password = make_password(passw)
            usuario.resetpass = True
            usuario.save()
            send_email_contrasena(cliente=usuario, password=passw)
            data['resp'] = True
        else:
            data['error'] = 'No existe usuario con ese numero de cedula'
        return HttpResponse(json.dumps(data), content_type='application/json')


import random
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str








