from django.shortcuts import render
from .models import Usuario,PerfilUsuario,Marca,Descuento,Prenda,Inventario,Pedido,DetallePedido,Reseña,Cesta
# Create your views here.
def index(request):
    return render(request, 'Tienda/index.html')

def lista_PerfilUsuario(request):
    perfiles=PerfilUsuario.objects.select_related("usuario").all()
    #perfiles=(PerfilUsuario.objects.raw("SELECT * FROM Tienda_perfilusuario p"
    #                                 +" JOIN Tienda_usuario u ON u.id = p.usuario_id"))
    return render(request,'Tienda/lista_perfil_usuario.html',{'lista_PerfilUsuario': perfiles})

def lista_Cesta(request):
    cesta=Cesta.objects.select_related("usuario").prefetch_related("prenda")
    cesta = cesta.order_by("fecha_creacion")
    return render(request,'Tienda/lista_cesta.html',{'lista_Cesta': cesta})