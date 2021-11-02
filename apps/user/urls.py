from django.urls import path
from . import views
from apps.user.views import *
from django.contrib.auth.decorators import login_required

app_name = 'Usuarios'

urlpatterns = [
    path('cliente/lista', lista.as_view(), name='lista_cliente'),
    path('cliente/reporte', report_cliente.as_view(), name='reporte_cliente'),
    path('cliente/nuevo', login_required(CrudView.as_view()), name='nuevo_cliente'),
    path('cliente/editar/<int:pk>', login_required(Updateview.as_view()), name='editar_cliente'),
    path('usuario/lista', lista_user.as_view(), name='lista_usuario'),
    path('usuario/reporte', report_user.as_view(), name='reporte_usuario'),
    path('usuario/nuevo', login_required(CrudView_user.as_view()), name='nuevo_usuario'),
    path('usuario/editar/<int:pk>', login_required(Updateview_user.as_view()), name='editar_usuario'),
    path('usuario/perfil', login_required(Profile.as_view()), name='perfil'),
    path('change_group/<int:pk>', login_required(UserChangeGroup.as_view()), name='user_change_group'),
    path('reset', views.ResetPass, name='Reset'),
    path('groups', login_required(Listgroupsview.as_view()), name='groups'),
    path('newgroup', login_required(CrudViewGroup.as_view()), name='newgroup'),
    path('grupo_editar/<int:pk>', login_required(UpdateGroup.as_view()), name='grupo_editar'),

    # path('profile', login_required(views.profile), name='profile'),

]
