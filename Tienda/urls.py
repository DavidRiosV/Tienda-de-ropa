from django.urls import path
from.import views

urlpatterns = [
        path('perfil_usuario/lista',views.lista_PerfilUsuario, name='lista_PerfilUsuario'),
]       