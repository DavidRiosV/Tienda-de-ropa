# Aplicación Web Parte I - Inicio y Modelos
# Descripción

**Eclipsados** es una página web desarrollada como proyecto académico utilizando **Django**. El sitio está enfocado en la venta de ropa alternativa y busca ofrecer una experiencia moderna y funcional que refleje la estética única de este estilo.

# Modelos y descripción

## 1. Usuario
Información básica de cada usuario registrado en la tienda.

### Atributos:
- `nombre` (CharField, max_length=200) → Nombre completo del usuario.
- `identificador` (PositiveIntegerField, unique=True) → ID único del usuario.
- `fecha_nacimiento` (DateField) → Fecha de nacimiento.
- `correo_electronico` (EmailField, unique=True) → Correo electrónico único.

### Relaciones:
- OneToOne con `PerfilUsuario`

## 2. PerfilUsuario
Información adicional del usuario.

### Atributos:
- `bio` (TextField, blank=True) → Breve biografía.
- `direccion` (CharField, max_length=255, blank=True) → Dirección del usuario.
- `telefono` (CharField, max_length=20, blank=True) → Número de teléfono.
- `sitio_web` (URLField, max_length=500, blank=True) → Página web del usuario.

### Relaciones:
- OneToOne con `Usuario`

## 3. Marca
Información sobre la marca de las prendas.

### Atributos:
- `nombre` (CharField, max_length=100, unique=True) → Nombre de la marca.
- `pais_origen` (CharField, max_length=100, blank=True) → País de origen.
- `descripcion` (TextField, blank=True) → Descripción de la marca.
- `año_fundacion` (PositiveIntegerField, null=True, blank=True) → Año de fundación.

### Relaciones:
- OneToMany con `Prenda`

## 4. Descuento
Información de descuentos aplicables a prendas.

### Atributos:
- `codigo` (CharField, max_length=20, unique=True) → Código del descuento.
- `porcentaje` (DecimalField, max_digits=5, decimal_places=2) → Porcentaje del descuento.
- `activo` (BooleanField, default=True) → Estado del descuento.
- `fecha_expiracion` (DateField) → Fecha de expiración del descuento.

### Relaciones:
- OneToMany con `Prenda`

## 5. Prenda
Información de cada prenda disponible en la tienda.

### Atributos:
- `nombre` (CharField, max_length=200) → Nombre de la prenda.
- `descripcion` (TextField, blank=True) → Descripción de la prenda.
- `talla` (CharField, max_length=3, choices=TALLAS) → Talla de la prenda.
- `color` (CharField, max_length=50) → Color de la prenda.
- `precio` (DecimalField, max_digits=8, decimal_places=2) → Precio.

### Relaciones:
- ManyToOne con `Marca`
- ManyToOne con `Descuento`
- OneToOne con `Inventario`
- ManyToMany con `Usuario`

## 6. Inventario
Control de stock de cada prenda.

### Atributos:
- `cantidad_disponible` (PositiveIntegerField, default=0) → Cantidad en stock.
- `ubicacion_almacen` (CharField, max_length=255, blank=True) → Ubicación física.
- `stock_minimo` (PositiveIntegerField, default=1) → Mínimo en stock.
- `stock_maximo` (PositiveIntegerField, default=100) → Máximo en stock.

### Relaciones:
- OneToOne con `Prenda`

## 7. Pedido
Pedidos realizados por usuarios.

### Atributos:
- `fecha` (DateTimeField, auto_now_add=True) → Fecha del pedido.
- `total` (DecimalField, max_digits=10, decimal_places=2, default=0) → Total del pedido.
- `estado` (CharField, max_length=4, choices=ESTADOS, default='PEND') → Estado del pedido.
- `direccion_envio` (CharField, max_length=255) → Dirección de envío.

### Relaciones:
- ManyToOne con `Usuario`
- ManyToMany con `Prenda` (a través de `DetallePedido`)

## 8. DetallePedido
Detalle de los productos en un pedido.

### Atributos:
- `cantidad` (PositiveIntegerField) → Cantidad de la prenda en el pedido.
- `precio` (DecimalField, max_digits=8, decimal_places=2) → Precio unitario.
- `fecha_agregado` (DateTimeField, auto_now_add=True) → Fecha de agregado al pedido.
- `fecha_entrega` (DateTimeField, auto_now_add=True) → Fecha estimada de entrega.

### Relaciones:
- OneToOne con `Pedido`
- ManyToOne con `Prenda`

## 9. Resena
Opiniones de los usuarios sobre las prendas.

### Atributos:
- `calificacion` (PositiveIntegerField) → Puntuación de la prenda.
- `comentario` (TextField, blank=True) → Comentario del usuario.
- `fecha` (DateTimeField, auto_now_add=True) → Fecha de la reseña.
- `recomendado` (BooleanField, default=True) → Recomendación.

### Relaciones:
- ManyToMany con `Usuario`
- ManyToOne con `Prenda`

## 10. Cesta
Cesta de compras de cada usuario.

### Atributos:
- `fecha_creacion` (DateTimeField, auto_now_add=True) → Fecha de creación.
- `activo` (BooleanField, default=True) → Estado de la cesta.
- `objetos_en_cesta` (DecimalField, max_digits=8, decimal_places=2, default=0) → Total de objetos.
- `precio` (DecimalField, max_digits=8, decimal_places=2, default=0) → Total de precio.

### Relaciones:
- ManyToOne con `Usuario`
- ManyToMany con `Prenda`

## Relaciones entre modelos

- Usuario ↔ PerfilUsuario 1 to 1
  Un usuario tiene un perfil y ese perfil pertenece solo a ese usuario.

- Pedido ↔ DetallePedido 1 to 1
  Un pedido tiene detalles y esos detalles pertenecen a ese pedido.

- Inventario ↔ Prenda 1 to 1
  Cada prenda tiene un inventario único y ese inventario pertenece solo a esa prenda.

- Prenda ↔ Marca 1 to many
  Una prenda pertenece a una marca y una marca puede tener muchas prendas.

- Prenda ↔ Descuento 1 to many
  Una prenda puede tener un descuento y un mismo descuento puede aplicarse a muchas prendas.

- Cesta ↔ Usuario 1 to many
  Una cesta pertenece a un usuario y un usuario puede tener varias cestas.

- Resena ↔ Usuario many to many
  Una reseña puede ser realizada por varios usuarios y un usuario puede escribir varias reseñas.

- Prenda ↔ Usuario many to many
  Una prenda puede pertenecer a varios usuarios y un usuario puede tener varias prendas.

- Pedido ↔ Prenda many to many
  Un pedido puede incluir varias prendas y una prenda puede estar en varios pedidos.
