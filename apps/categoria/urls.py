from django.urls import path

from apps.categoria.views import *
from django.contrib.auth.decorators import login_required
app_name = 'Categoria'

urlpatterns = [
    path('lista', login_required(lista.as_view()), name='lista'),
    path('nuevo', login_required(CrudView.as_view()), name='nuevo'),
    path('editar/<int:pk>', login_required(UpdateView.as_view()), name='editar'),
    path('eliminar/<int:pk>', login_required(DeleteView.as_view()), name='eliminar'),

]
