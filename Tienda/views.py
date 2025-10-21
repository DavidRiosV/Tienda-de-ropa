from django.shortcuts import render
from .models import Usuario,PerfilUsuario
from django.views.defaults import page_not_found
# Create your views here.
def index(request):
    return render(request, 'Tienda/index.html')

def lista_PerfilUsuario(request):
    perfiles=PerfilUsuario.objects.select_related("usuario").all()
    #perfiles=(PerfilUsuario.objects.raw("SELECT * FROM Tienda_perfilusuario p"
    #                                 +" JOIN Tienda_usuario u ON u.id = p.usuario_id"))
    return render(request,'Tienda/lista_perfil_usuario.html',{'lista_PerfilUsuario': perfiles})

def mi_error_404(request,exception=None):
    return render(request, 'Errores/404.html',None,None,404)

def mi_error_400(request, exception=None):
    return render(request, 'errors/400.html', None,None,400)

def mi_error_403(request, exception=None):
    return render(request, 'errors/403.html', None,None,403)

def mi_error_500(request):
    return render(request, 'errors/500.html', None,None,500)