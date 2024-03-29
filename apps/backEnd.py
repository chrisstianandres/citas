import json
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from os import urandom
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES as Algorithm
from cryptography.hazmat.primitives.ciphers.modes import ECB as Mode
from django.contrib.auth import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import *
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt




# -----------------------------------------------PAGINA PRINCIPAL-----------------------------------------------------#
# from apps.user.forms import UserForm, UserForm_online

from apps.empleado.models import Empleado
from apps.empresa.models import Empresa
from apps.producto.models import Producto, envio_stock_dia
from apps.user.forms import UserForm_cliente
from apps.user.models import User
from apps.compra.models import Detalle_compra



def nombre_empresa():
    if Empresa.objects.filter(id=1).exists():
        empresa = Empresa.objects.first()
    else:
        empresa = {'nombre': 'Sin nombre'}
    return empresa


def permisos(request):
    return request.session.groups.permissions.all()


def menu(request):
    if request.method == 'GET':
        request.user.get_group_session()
    data = {
        'titulo': 'Menu Principal', 'empresa': nombre_empresa(),
        'icono': 'fas fa-tachometer-alt', 'entidad': 'Menu Principal',
    }
    if not envio_stock_dia.objects.filter(fecha=datetime.now(), enviado=True).exists():
        repor = []
        for p in Producto.objects.all():
            stock = Detalle_compra.objects.filter(compra__estado=1, producto_id=p.id).aggregate(stock=Coalesce(Sum('stock_actual'), 0)).get('stock')
            if stock <= 5:
                item = p.toJSON()
                item['stock'] = stock
                repor.append(item)
        if len(repor) > 0:
            send_email(repor)
            envio_stock_dia(fecha=datetime.now(), enviado=True).save()
    prod = []
    for p in Producto.objects.all():
        stock = Detalle_compra.objects.filter(compra__estado=1, producto_id=p.id).aggregate(stock=Coalesce(Sum('stock_actual'), 0)).get('stock')
        if stock <= 5:
            item = p.toJSON()
            item['stock'] = stock
            prod.append(item)
    data['productos_stock_bajo'] = prod
    data['empleados'] = Empleado.objects.filter(estado=0)
    return render(request, 'front-end/index.html', data)


# -----------------------------------------------LOGEO----------------------------------------------------------------#

def logeo(request):
    data = {}
    if not request.user.is_authenticated:
        data['titulo'] = 'Inicio de Sesion'
        data['nomb'] = nombre_empresa()
        data['form'] = UserForm_cliente()
    else:
        return HttpResponseRedirect("/menu")
    return render(request, 'front-end/login.html', data)


@csrf_exempt
def cliente_add(request):
    data = {}
    f = UserForm_cliente(request.POST)
    datos = request.POST
    if f.is_valid():
        with transaction.atomic():
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
                permission = Permission.objects.get(codename='add_venta')
                permission2 = Permission.objects.get(codename='view_venta')
                use.user_permissions.add(permission)
                use.user_permissions.add(permission2)
                # venta.add_venta

                # u.user_permissions.add(permission)
                data['resp'] = 'error'
            else:
                f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
                data['error'] = f.errors
    else:
        data['error'] = f.errors
    return HttpResponse(json.dumps(data), content_type="application/json")


# class signin(TemplateView):
#     form_class = UserForm_online
#     template_name = 'front-end/signin.html'
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         action = request.POST['action']
#         try:
#             if action == 'add':
#                 f = UserForm_online(request.POST, request.FILES)
#                 if f.is_valid():
#                     f.save(commit=False)
#                     if verificar(f.data['cedula']):
#                         user = f.save()
#                         # print(user.id)
#
#                         return HttpResponseRedirect('/login')
#                     else:
#                         f.add_error("cedula", "Numero de Cedula no valido para Ecuador")
#                         data['form'] = f
#                 else:
#                     data['title'] = 'Registro de usuario'
#                     data['nomb'] = nombre_empresa()
#                     data['crud'] = '/signin/'
#                     data['action'] = 'add'
#                     data['error'] = f.errors
#                     data['form'] = f
#                     return render(request, 'front-end/signin.html', data)
#             else:
#                 data['error'] = 'No ha seleccionado ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return HttpResponse(json.dumps(data), content_type='application/json')
#
#     def get(self, request, *args, **kwargs):
#         data = {}
#         if not self.request.user.is_authenticated:
#             data['title'] = 'Registro de usuario'
#             data['nomb'] = nombre_empresa()
#             data['form'] = UserForm_online()
#             data['crud'] = '/signin/'
#             data['action'] = 'add'
#         else:
#             return HttpResponseRedirect("/")
#         return render(request, self.template_name, data)
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['title'] = 'Registro de usuario'
#         data['nomb'] = nombre_empresa()
#         data['form'] = UserForm_online()
#         data['crud'] = '/signin/'
#         data['action'] = 'add'
#         return data

@csrf_exempt
def send_email(productos):
    data = {}
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mailServer.starttls()
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        email_to = 'chrisstianandres@gmail.com'
        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = 'Stock bajo de productos'
        empresa = nombre_empresa()
        content = render_to_string('front-end/user/email_stock.html', {
            'productos': productos,
            'empresa': empresa
        })
        mensaje.attach(MIMEText(content, 'html'))
        mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, mensaje.as_string())
    except Exception as e:
        data['error'] = str(e)
    return data

@csrf_exempt
def send_email_contrasena(cliente, password):
    data = {}
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        mailServer.starttls()
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        email_to = cliente.email
        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = 'Reseteo de Contraseña'
        empresa = nombre_empresa()
        content = render_to_string('front-end/user/send_email_password.html', {
            'cliente': cliente,
            'empresa': empresa,
            'pass': password
        })
        mensaje.attach(MIMEText(content, 'html'))
        mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, mensaje.as_string())
    except Exception as e:
        print('AQUI ESTA EL ERROR'+str(e))
        data['error'] = str(e)
    return data


@csrf_exempt
def connect(request):
    data = {}
    if request.method == 'POST' or None:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.estado == 1:
                login(request, user)
                data['resp'] = True
                data['reset'] = user.resetpass
            else:
                data['error'] = '<strong>Usuario Inactivo </strong>'
        else:
            data['error'] = '<strong>Usuario o contraseña no validos </strong><br>'
    else:
        data['error'] = 'Metodo Request no es Valido.'
    return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def disconnect(request):
    data = []
    logout(request)
    return HttpResponse(json.dumps(data))


@csrf_exempt
def check_ced(request):
    data = {}
    nro = request.POST['data']
    if verificar(nro):
        data['resp'] = True
    else:
        data['error'] = "Numero de Cedula no valido para Ecuador"
    return JsonResponse(data)


@csrf_exempt
def verificar(nro):
    l = len(nro)
    if l == 10 or l == 13:  # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 22:  # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6:  # numeros enter 0 y 6
                if l == 10:
                    return __validar_ced_ruc(nro, 0)
                elif l == 13:
                    return __validar_ced_ruc(nro, 0) and nro[
                                                         10:13] != '000'  # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                return __validar_ced_ruc(nro, 1)  # sociedades publicas
            elif tercer_dig == 9:  # si es ruc
                return __validar_ced_ruc(nro, 2)  # sociedades privadas
            else:
                error = 'Tercer digito invalido'
                return False and error
        else:
            error = 'Codigo de provincia incorrecto'
            return False and error
    else:
        error = 'Longitud incorrecta del numero ingresado'
        return False and error


def __validar_ced_ruc(nro, tipo):
    total = 0
    if tipo == 0:  # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])  # digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1:  # r.u.c. publicos
        base = 11
        d_ver = int(nro[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2)
    elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(nro[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0, len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
        else:
            total += p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver


class PrimaryKeyEncryptor:
    def __init__(self, secret: str):
        secret_bytes = bytes.fromhex(secret)

        if len(secret_bytes) != 16:
            raise ValueError('The secret for the PrimaryKeyEncryptor must be 16 bytes in hexadecimal format')

        algorithm = Algorithm(secret_bytes)
        mode = Mode()

        self.cipher = Cipher(algorithm, mode, backend=default_backend())

    @staticmethod
    def generate_secret() -> str:
        return urandom(16).hex()

    def encrypt(self, primary_key: int) -> str:
        primary_key_bytes = primary_key.to_bytes(8, byteorder='big')

        encryptor = self.cipher.encryptor()

        cipher_bytes = encryptor.update(primary_key_bytes * 2) + encryptor.finalize()

        return cipher_bytes.hex()

    def decrypt(self, encrypted_primary_key: str) -> int:
        cipher_bytes = bytes.fromhex(encrypted_primary_key)

        if len(cipher_bytes) != 16:
            raise ValueError('The encrypted primary key must be 16 bytes in hexadecimal format')

        decryptor = self.cipher.decryptor()

        plain_bytes = decryptor.update(cipher_bytes) + decryptor.finalize()

        if plain_bytes[:8] != plain_bytes[8:]:
            raise ValueError('The encrypted primary key is invalid')

        return int.from_bytes(plain_bytes[:8], byteorder='big')
