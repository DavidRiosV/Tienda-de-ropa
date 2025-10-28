from django.shortcuts import render
from .models import Usuario,PerfilUsuario,Marca,Descuento,Prenda,Inventario,Pedido,DetallePedido,Reseña,Cesta
from django.db.models import Q,Prefetch,Sum


def index(request):
    return render(request, 'Tienda/index.html')

def lista_PerfilUsuario(request):
    perfiles=PerfilUsuario.objects.select_related("usuario").all()
    #perfiles=(PerfilUsuario.objects.raw("SELECT * FROM Tienda_perfilusuario p"
    #                                 +" JOIN Tienda_usuario u ON u.id = p.usuario_id"))
    return render(request,'Tienda/lista_perfil_usuario.html',{'lista_PerfilUsuario': perfiles})

def lista_Cesta(request):
    cestas = Cesta.objects.select_related("usuario").prefetch_related("prenda").order_by("fecha_creacion")
    '''
    cestas = Cesta.objects.raw("SELECT* FROM Tienda_cesta c "
       " JOIN Tienda_usuario u ON u.id = c.usuario_id"
       " JOIN Tienda_cesta_prenda cp ON cp.cesta_id = c.id"
       " JOIN Tienda_prenda p ON p.id = cp.prenda_id"
       " ORDER BY c.fecha_creacion"
    #)
    '''
    return render(request, 'Tienda/lista_cesta.html', {'lista_Cesta': cestas})

def dame_usuario(request, id_usuario):
    usuario = Usuario.objects.select_related("perfil").prefetch_related("prendas", "reseñas").get(id=id_usuario)
    ''' 
    usuario = Usuario.objects.raw("SELECT * FROM Tienda_usuario u "
                                  " JOIN Tienda_perfilusuario pu ON pu.id = u_id"
                                  " JOIN Tienda_prenda_usuarios pus ON pus.id = u_id"
                                  " JOIN Tienda_reseña_usuarios ru ON ru.id = u_id"
                                  " WHERE u.id=%s,[id_usuario])"[0]
    )
    '''
    return render(request, 'Tienda/dame_usuario_.html', {'dame_usuario': usuario})  

def lista_descuentos(request, porcentaje):
    descuentos = Descuento.objects.prefetch_related("prendas")
    descuentos = descuentos.filter(Q(porcentaje=porcentaje) | Q(porcentaje=25)).order_by("fecha_expiracion")
    ''' 
    descuentos = Descuento.objects.raw("SELECT * FROM Tienda_descuento d "
                                       " JOIN Tienda_prenda p ON p.descuento_id = d.id "  
                                       "WHERE d.porcentaje = %s OR d.porcentaje = %s "
                                       "ORDER BY d.fecha_expiracion",[porcentaje,25])
    '''
    return render(request, 'Tienda/lista_descuentos.html', {'lista_descuentos': descuentos})


def lista_marcas(request, palabra, pais):
    marcas = Marca.objects.prefetch_related("prendas")
    marcas = marcas.filter(descripcion__contains=palabra, pais_origen=pais)
    '''
    marcas = Marca.objects.raw("SELECT * FROM Tienda_marca m "
            +" JOIN Tienda_prenda p ON p.marca_id = m.id  "
            +" WHERE m.pais_origen = %s "
            +" AND  m.descripcion LIKE %s",[pais,"%"+palabra+"%"])
    '''
    return render(request, 'Tienda/lista_marcas.html', {'lista_marcas': marcas})

def lista_prendas(request):
    prendas = Prenda.objects.select_related('marca', 'descuento').prefetch_related('usuarios').filter(usuarios__isnull=True).order_by('nombre')
    '''
    prendas = Prenda.objects.raw("SELECT * FROM Tienda_prenda p"
                                 " JOIN Tienda_marca m ON m.id =p.marca_id"
                                 " JOIN Tienda_descuento d ON d.id =p.descuento_id"
                                 " LEFT JOIN Tienda_prenda_usuarios pu ON pu.prenda_id = p.id"
                                 " WHERE pu.id IS NULL"
                                 " ORDER BY p.nombre"
    )
    '''
    return render(request, 'Tienda/lista_prendas.html', {'lista_prendas': prendas})

def lista_reseñas(request):
    reseñas = Reseña.objects.select_related("prenda").prefetch_related("usuarios").order_by('-fecha')[:3]
    '''
    reseñas = Reseña.objects.raw("SELECT * FROM Tienda_reseña r"
                                " JOIN Tienda_prenda p ON p.id = r.prenda_id"
                                " LEFT JOIN Tienda_prenda_usuarios pu ON pu.prenda_id= r.id"
                                " ORDER BY r.fecha")[:3]
    '''
    return render(request, 'Tienda/lista_reseñas.html', {'lista_reseñas': reseñas})

def lista_pedido_prendas(request, id_pedido):
    pedido = Pedido.objects.prefetch_related(Prefetch("prenda")).get(id=id_pedido)
    '''
    pedido = Pedido.objects.raw("SELECT * FROM Tienda_pedido p"
                                " INNER JOIN Tienda_detallepedido dp ON dp.pedido_id = p.id"
                                " WHERE p.id = %s",[id_pedido])
    '''
    return render(request, 'Tienda/lista_pedido_prendas.html', {"pedido": pedido})

def lista_detallepedido_total(request):
    total_precio = DetallePedido.objects.aggregate(total=Sum('precio'))
    detalles = DetallePedido.objects.select_related('pedido', 'prenda').all()
    ''' 
    detalles = DetallePedido.objects.raw("SELECT * FROM Tienda_detallepedido dp "
                                         " JOIN Tienda_pedido p ON p.id = dp.pedido_id"
                                         " JOIN Tienda_prenda pr ON pr.id = dp.prenda_id"
    )
    total_precio= DetallePedido.objects.raw("SELECT sum(dp.precio) as total FROM Tienda_detallepedido dp" )
    '''
    return render(request, 'Tienda/lista_detallepedido_total.html', {'detalles': detalles,'total_precio': total_precio['total']})

def inventario_minimo(request, minimo_stock):
    minimo_stock = int(minimo_stock)
    inventarios = Inventario.objects.filter(cantidad_disponible__lte=minimo_stock).select_related('prenda')
    '''
    inventarios = Inventario.objects.raw("SELECT * FROM Tienda_inventario i"
                                         " JOIN Tienda_prenda p ON p.id = i.prenda_id"
                                         " WHERE i.cantidad_disponible <=%s",[minimo_stock]
    )
    '''
    return render(request, 'Tienda/inventario_minimo.html', {"inventarios": inventarios,"minimo_stock": minimo_stock})

def mi_error_404(request,exception=None):
    return render(request, 'Errores/404.html',None,None,404)

def mi_error_400(request, exception=None):
    return render(request, 'errors/400.html', None,None,400)

def mi_error_403(request, exception=None):
    return render(request, 'errors/403.html', None,None,403)

def mi_error_500(request):
    return render(request, 'errors/500.html', None,None,500)