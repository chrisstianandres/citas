from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from apps.Mixins import SuperUserRequiredMixin, ValidatePermissionRequiredMixin
from apps.backEnd import nombre_empresa
from apps.servicio.forms import ServicioForm
from apps.servicio.models import Servicio

opc_icono = 'fas fa-concierge-bell'
opc_entidad = 'Servicios'
crud = '/servicio/crear'
empresa = nombre_empresa()


class lista(ValidatePermissionRequiredMixin, ListView):
    model = Servicio
    template_name = 'front-end/servicio/servicio_list.html'
    permission_required = 'view_servicio'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['icono'] = opc_icono
        data['entidad'] = opc_entidad
        data['boton'] = 'Nuevo Servicio'
        data['titulo'] = 'Listado de Servicios'
        data['nuevo'] = '/servicio/nuevo'
        data['empresa'] = empresa
        return data


def nuevo(request):
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
        'boton': 'Guardar Servicio', 'action': 'add', 'titulo': 'Nuevo Registro de un Servicio',
    }
    if request.method == 'GET':
        data['form'] = ServicioForm()
    return render(request, 'front-end/servicio/servicio_form.html', data)


def crear(request):
    f = ServicioForm(request.POST)
    data = {
        'icono': opc_icono, 'entidad': opc_entidad, 'crud': crud, 'empresa': empresa,
        'boton': 'Guardar Servicio', 'action': 'add', 'titulo': 'Nuevo Registro de un Servicio'
    }
    if request.method == 'POST':
        f = ServicioForm(request.POST)
        if f.is_valid():
            f.save()
        else:
            data['form'] = f
            return render(request, 'front-end/servicio/servicio_form.html', data)
        return HttpResponseRedirect('/servicio/lista')


def editar(request, id):
    servicio = Servicio.objects.get(id=id)
    crud = '/servicio/editar/' + str(id)
    data = {
        'icono': opc_icono, 'crud': crud, 'entidad': opc_entidad, 'empresa': empresa,
        'boton': 'Guardar Edicion', 'titulo': 'Editar Registro de un Servicio',
    }
    if request.method == 'GET':
        form = ServicioForm(instance=servicio)
        data['form'] = form
    else:
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
        else:
            data['form'] = form
        return redirect('/servicio/lista')
    return render(request, 'front-end/servicio/servicio_form.html', data)


@csrf_exempt
def eliminar(request):
    data = {}
    try:
        id = request.POST['id']
        if id:
            ps = Servicio.objects.get(pk=id)
            ps.delete()
            data['resp'] = True
        else:
            data['error'] = 'Ha ocurrido un error'
    except Exception as e:
        data['error'] = "!No se puede eliminar este Servicio porque esta referenciado en otros procesos!!"
        data['content'] = "Intenta con otro Servicio"
    return JsonResponse(data)