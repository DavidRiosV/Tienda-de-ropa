from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    identificador = models.PositiveIntegerField(unique=True)
    fecha_nacimiento = models.DateField()
    correo_electronico = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.identificador})"

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(Usuario,on_delete=models.CASCADE,related_name='perfil')

    bio = models.TextField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    sitio_web = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.nombre}"

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    pais_origen = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    año_fundacion = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Descuento(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_expiracion = models.DateField()

    def __str__(self):
        return f"{self.codigo} ({self.porcentaje}%)"

class Prenda(models.Model):
    TALLAS = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'XXL'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    talla = models.CharField(max_length=3, choices=TALLAS)
    color = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)

    marca = models.ForeignKey(Marca,on_delete=models.CASCADE,related_name='prendas')
    descuento = models.ForeignKey(Descuento,on_delete=models.SET_NULL,null=True,blank=True,related_name='prendas')
    usuarios = models.ManyToManyField(Usuario,related_name='prendas')

    def __str__(self):
        return f"{self.nombre} - {self.talla} - {self.color}"

class Inventario(models.Model):
    prenda = models.OneToOneField(Prenda,on_delete=models.CASCADE,related_name='inventario')

    cantidad_disponible = models.PositiveIntegerField(default=0)
    ubicacion_almacen = models.CharField(max_length=255, blank=True)
    stock_minimo = models.PositiveIntegerField(default=1)
    stock_maximo = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"Inventario de {self.prenda.nombre}"

class Pedido(models.Model):
    ESTADOS = [
        ('PEND', 'Pendiente'),
        ('PROC', 'Procesando'),
        ('ENV', 'Enviado'),
        ('ENT', 'Entregado'),
    ]

    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name='pedidos')

    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=4, choices=ESTADOS, default='PEND')
    direccion_envio = models.CharField(max_length=255)

    prenda = models.ManyToManyField(Prenda,through='DetallePedido',related_name='pedidos')

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.nombre}"

class DetallePedido(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='detalle')
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE)

    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.cantidad}x {self.prenda.nombre} en pedido {self.pedido.id}"

class Reseña(models.Model):
    usuarios = models.ManyToManyField(Usuario,related_name='reseñas')
    prenda = models.ForeignKey(Prenda,on_delete=models.CASCADE,related_name='reseñas')

    calificacion = models.PositiveIntegerField()
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    recomendado = models.BooleanField(default=True)

    def __str__(self):
        return f"Reseña de {self.prenda.nombre}"

class Cesta(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name='cestas')
    prenda = models.ManyToManyField(Prenda, related_name='cestas')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    objetos_en_cesta = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Cesta de {self.usuario.nombre}"
