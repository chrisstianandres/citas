import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.backEnd import nombre_empresa, verificar
from apps.empleado.forms import EmpleadoForm
from apps.empleado.models import Empleado
from apps.mixins import ValidatePermissionRequiredMixin
# from apps.ubicacion.models import *

opc_icono = 'fas fa-people-carry'
opc_entidad = 'Empleados'
crud = '/empleado/nuevo'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Empleado
    template_name = "front-end/empleado/list.html"
    permission_required = 'empleado.view_empleado'

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'list':
                data = []
                for c in Empleado.objects.all():
                    data.append(c.toJSON())
            elif action == 'search':
                data = []
                term = request.POST['term']
                query = Empleado.objects.filter(
                    Q(nombres__icontains=term) | Q(apellidos__icontains=term) | Q(cedula__icontains=term))[0:10]
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
        data['titulo'] = 'Empleados'
        data['titulo_lista'] = 'Listado de Empleados'
        data['titulo_formulario'] = 'Formulario de Registro'
        data['form'] = EmpleadoForm
        data['nuevo'] = '/empleado/nuevo'
        data['empresa'] = empresa
        return data


class CrudView(ValidatePermissionRequiredMixin, TemplateView):
    form_class = EmpleadoForm
    model = Empleado
    template_name = 'front-end/empleado/form.html'
    permission_required = 'empleado.add_empleado'

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
            if verificar(f.data['cedula']):
                cli = f.save()
                data['resp'] = True
                data['empleado'] = cli.toJSON()
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
        data['titulo'] = 'Nueva Presentacion'
        data['nuevo'] = '/presentacion/nuevo'
        data['action'] = 'add'
        data['empresa'] = empresa
        data['form'] = self.form_class
        return data


class UpdateView(ValidatePermissionRequiredMixin, UpdateView):
    form_class = EmpleadoForm
    model = Empleado
    template_name = 'front-end/empleado/form.html'
    permission_required = 'empleado.change_empleado'

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
            if verificar(f.data['cedula']):
                cli = f.save()
                data['resp'] = True
                data['empleado'] = cli.toJSON()
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
        data['titulo'] = 'Editar una Empleado'
        data['action'] = 'edit'
        data['empresa'] = empresa
        dato = self.model.objects.get(pk=self.kwargs['pk'])
        data['form'] = self.form_class(instance=dato)
        return data


class DeleteView(ValidatePermissionRequiredMixin, DeleteView):
    model = Empleado
    permission_required = 'empleado.delete_empleado'

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


class report(ValidatePermissionRequiredMixin, ListView):
    model = Empleado
    template_name = 'front-end/cliente/report.html'
    permission_required = 'cliente.view_cliente'

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
        data['entidad'] = 'Reporte de Empleados'
        data['titulo'] = 'Reporte de Empleados'
        data['empresa'] = empresa
        return data



# def ciudad(request):
#     data = {}
#     with open('D:/PycharmProjects/ferreteria/apps/ciudades.json', encoding="utf8") as f:
#         data = json.load(f)
#         for c in data:
#             pro = Provincia()
#             pro.nombre = str(data[c]['provincia'])
#             pro.save()
#             for x in data[c]['cantones']:
#                 can = Canton()
#                 can.provincia_id = pro.id
#                 can.nombre = str(data[c]['cantones'][x]['canton'])
#                 can.save()
#                 for p in data[c]['cantones'][x]['parroquias']:
#                     par = Parroquia()
#                     par.canton_id = can.id
#                     par.nombre = str(data[c]['cantones'][x]['parroquias'][p])
#                     par.save()
#         data = Parroquia.objects.all()
#     return HttpResponse(data)