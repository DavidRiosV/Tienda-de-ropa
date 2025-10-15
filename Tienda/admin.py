from django.contrib import admin
from .models import (
    Usuario,
    PerfilUsuario,
    Marca,
    Descuento,
    Prenda,
    Inventario,
    Pedido,
    DetallePedido,
    Reseña,
    Cesta
)

admin.site.register(Usuario)
admin.site.register(PerfilUsuario)
admin.site.register(Marca)
admin.site.register(Descuento)
admin.site.register(Prenda)
admin.site.register(Inventario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Reseña)
admin.site.register(Cesta)
