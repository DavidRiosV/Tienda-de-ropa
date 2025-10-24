from django.urls import path,include
from.import views

urlpatterns = [
        path('',views.index,name='index.html'),
        path('perfil_usuario/lista',views.lista_PerfilUsuario, name='lista_PerfilUsuario'),
        path('cesta/lista',views.lista_Cesta, name='lista_Cesta'),
        path('usuario/<int:id_usuario>/', views.dame_usuario, name='dame_usuario'),
        path('descuento/<int:porcentaje>/', views.lista_descuentos, name='lista_descuentos'),
        path('marcas/<str:palabra>/<str:pais>', views.lista_marcas, name='lista_marcas'),
        path("__debug__/", include("debug_toolbar.urls")),

]