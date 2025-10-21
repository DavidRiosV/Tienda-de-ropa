from django.urls import path
from.import views

urlpatterns = [
        path('',views.index,name='index.html'),
        path('perfil_usuario/lista',views.lista_PerfilUsuario, name='lista_PerfilUsuario'),
        path('cesta/lista',views.lista_Cesta, name='lista_Cesta'),
        path('usuario/<int:usuario_id>/prendas/', views.prendas_usuario, name='prendas_usuario'),
]               