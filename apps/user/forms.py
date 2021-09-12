from datetime import *

from django import forms
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.forms import TextInput, EmailInput, SelectMultiple

from .models import User
from django.contrib.auth.models import Group


class UserForm(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            # self.fields[field].widget.attrs.update({
            #     'class': 'form-control'
            # })

            self.fields['first_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos nombres', 'class': 'form-control form-rounded'})
            self.fields['last_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos Apellidos', 'class': 'form-control form-rounded'})
            self.fields['cedula'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de cedula', 'class': 'form-control form-rounded'})
            self.fields['email'].widget = EmailInput(
                attrs={'placeholder': 'abc@correo.com', 'class': 'form-control form-rounded'})
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingresa una direccion', 'class': 'form-control form-rounded'})
            self.fields['telefono'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un numero de telefono', 'class': 'form-control form-rounded'})
            self.fields['celular'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un numero de celular', 'class': 'form-control form-rounded'})
            self.fields['username'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un nombre de usuario', 'class': 'form-control form-rounded'})
            self.fields['sexo'].widget.attrs = {
                'class': 'form-control select2'
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'cedula',
                  'email',
                  'avatar',
                  'sexo',
                  'telefono',
                  'celular',
                  'direccion',
                  'password'
                  ]
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'cedula': 'N° de cedula',
            'email': 'Correo',
            'avatar': 'Imagen',
            'sexo': 'Genero',
            'telefono': 'Telefono',
            'celular': 'Celular',
            'direccion': 'Direccion',
            'password': 'Contraseña',

        }
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'cedula': forms.TextInput(),
            'sexo': forms.Select(),
            'correo': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'celular': forms.TextInput(),
            'direccion': forms.Textarea(),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserForm_online(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            # self.fields[field].widget.attrs.update({
            #     'class': 'form-control'
            # })

            self.fields['first_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos nombres', 'class': 'form-control form-rounded'})
            self.fields['last_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos Apellidos', 'class': 'form-control form-rounded'})
            self.fields['cedula'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de cedula', 'class': 'form-control form-rounded'})
            self.fields['telefono'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un numero de telefono', 'class': 'form-control form-rounded'})
            self.fields['celular'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un numero de celular', 'class': 'form-control form-rounded'})
            self.fields['email'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un correo', 'class': 'form-control form-rounded'})
            self.fields['username'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un nombre de usuario', 'class': 'form-control form-rounded'})
            self.fields['sexo'].widget.attrs = {
                'class': 'form-control select2'
            }
            # self.fields["fecha_nacimiento"].widget = SelectDateWidget(years=years,
            #                                                         attrs={'class': 'selectpicker'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'cedula',
                  'sexo',
                  'telefono',
                  'celular',
                  'password',

                  ]
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo',
            'cedula': 'N° de cedula',
            'sexo': 'Genero',
            'telefono': 'Telefono',
            'celular': 'Celular',
            'direccion': 'Direccion',
            'password': 'Contraseña',


        }
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'cedula': forms.TextInput(),
            'sexo': forms.Select(),
            'telefono': forms.TextInput(),
            'celular': forms.TextInput(),
            'direccion': forms.Textarea(),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
        }

    @transaction.atomic()
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                # nombres = self.cleaned_data['first_name']
                # apellidos = self.cleaned_data['last_name']
                # cedula = self.cleaned_data['cedula']
                # sexo = self.cleaned_data['sexo']
                # telefono = self.cleaned_data['telefono']
                # correo = self.cleaned_data['email']
                u.save()
                # grupo = Group.objects.get(name__icontains='cliente')
                # usersave = User.objects.get(id=u.id)
                # usersave.groups.add(grupo)
                # usersave.tipo = 0
                # usersave.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserForm_cliente(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            # self.fields[field].widget.attrs.update({
            #     'class': 'form-control'
            # })

            self.fields['first_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese su nombre', 'class': 'form-control form-rounded'})
            self.fields['last_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese su apellido', 'class': 'form-control form-rounded'})
            self.fields['cedula'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de cedula', 'class': 'form-control form-rounded'})
            self.fields['email'].widget = EmailInput(
                attrs={'placeholder': 'abc@correo.com', 'class': 'form-control form-rounded'})
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingresa una direccion', 'class': 'form-control form-rounded'})
            self.fields['telefono'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un numero de telefono', 'class': 'form-control form-rounded'})
            self.fields['celular'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un numero de celular', 'class': 'form-control form-rounded'})
            self.fields['sexo'].widget.attrs = {
                'class': 'form-control select2'
            }

            # self.fields["fecha_nacimiento"].widget = SelectDateWidget(years=years,
            #                                                         attrs={'class': 'selectpicker'})
        # habilitar, desabilitar, y mas

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'cedula',
                  'email',
                  'sexo',
                  'telefono',
                  'celular',
                  'direccion'
                  ]
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'cedula': 'N° de cedula',
            'email': 'Correo',
            'sexo': 'Genero',
            'telefono': 'Telefono',
            'celular': 'Celular',
            'direccion': 'Direccion'
        }
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'cedula': forms.TextInput(),
            'sexo': forms.Select(),
            'correo': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'celular': forms.TextInput(),
            'direccion': forms.Textarea()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                u = form.save(commit=False)
                if u.pk is None:
                    ced = self.cleaned_data['cedula']
                    nombre = self.cleaned_data['first_name']
                    apellido = self.cleaned_data['last_name']
                    sex = self.cleaned_data['sexo']
                    correo = self.cleaned_data['email']
                    telefono = self.cleaned_data['telefono']
                    celular = self.cleaned_data['celular']
                    direccion = self.cleaned_data['direccion']
                    use = User()
                    use.username = ced
                    use.cedula = ced
                    use.first_name = nombre
                    use.last_name = apellido
                    use.sexo = sex
                    use.email = correo
                    use.telefono = telefono
                    use.celular = celular
                    use.direccion = direccion
                    use.tipo = 0
                    use.password = make_password(ced)
                    use.save()
                    grupo = Group.objects.get(name__icontains='cliente')
                    usersave = User.objects.get(id=u.id)
                    usersave.groups.add(grupo)
                    usersave.save()
                    return use
                else:
                    u.save()
                    if Group.objects.filter(name__icontains='cliente').exists():
                        grupo = Group.objects.get(name__icontains='cliente')
                        usersave = User.objects.get(id=u.id)
                        if u.tipo == 0:
                            if not usersave.groups.filter(name='cliente').exists():
                                usersave.groups.add(grupo)
                                usersave.save()
                return u
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserForm_profile(forms.ModelForm):
    # constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this_year = datetime.now().year
        years = range(this_year - 15, this_year - 3)
        for field in self.Meta.fields:
            self.fields['first_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos nombres', 'class': 'form-control form-rounded'})
            self.fields['last_name'].widget = TextInput(
                attrs={'placeholder': 'Ingrese sus dos Apellidos', 'class': 'form-control form-rounded'})
            self.fields['cedula'].widget = TextInput(
                attrs={'placeholder': 'Ingrese numero de cedula', 'class': 'form-control form-rounded'})
            self.fields['email'].widget = EmailInput(
                attrs={'placeholder': 'abc@correo.com', 'class': 'form-control form-rounded'})
            self.fields['direccion'].widget = TextInput(
                attrs={'placeholder': 'Ingresa una direccion', 'class': 'form-control form-rounded'})
            self.fields['telefono'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un numero de telefono', 'class': 'form-control form-rounded'})
            self.fields['celular'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un numero de celular', 'class': 'form-control form-rounded'})
            self.fields['username'].widget = TextInput(
                attrs={'placeholder': 'Ingresa un nombre de usuario', 'class': 'form-control form-rounded'})
            self.fields['sexo'].widget.attrs = {
                'class': 'form-control select2'
            }
        # habilitar, desabilitar, y mas

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'cedula',
                  'email',
                  'avatar',
                  'sexo',
                  'telefono',
                  'celular',
                  'direccion'
                  ]
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'cedula': 'N° de cedula',
            'email': 'Correo',
            'avatar': 'Imagen',
            'sexo': 'Genero',
            'telefono': 'Telefono',
            'celular': 'Celular',
            'direccion': 'Direccion'
        }
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'cedula': forms.TextInput(),
            'sexo': forms.Select(),
            'correo': forms.EmailInput(),
            'telefono': forms.TextInput(),
            'celular': forms.TextInput(),
            'direccion': forms.Textarea()
        }


class UserForm_password(forms.ModelForm):
    # constructor
    class Meta:
        model = User
        fields = ['password']
        labels = {'password': 'Nueva Contraseña'}
        widgets = {'password': forms.PasswordInput(attrs={'class': 'form-control'})}

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data