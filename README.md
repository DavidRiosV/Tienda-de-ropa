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
- Pedido ↔ DetallePedido 1 to 1
- Inventario ↔ Prenda 1 to 1
- Prenda ↔ Marca 1 to many
- Prenda ↔ Descuento 1 to many
- Cesta ↔ Usuario 1 to many
- Resena ↔ Usuario many to many
- Prenda ↔ Usuario many to many
- Pedido ↔ Prenda many to many

# Vistas y URLS

## 1. lista_PerfilUsuario
Muestra todos los perfiles de los usuarios junto con el nombre del usuario al que pertenece cada perfil.  
Utiliza `select_related` para optimizar la relación con el modelo **Usuario**.

## 2. lista_Cesta
Muestra todas las cestas registradas junto con sus datos relacionados: el usuario al que pertenece cada cesta y las prendas que contiene.  
Además, las cestas aparecen **ordenadas por el atributo `fecha_creacion`** (de más antiguas a más recientes).

## 3. dame_usuario
Muestra la información completa de un usuario específico según el **ID que se le pase por parámetro**.  
Incluye sus datos personales, su perfil, las prendas asociadas y las reseñas que haya publicado.

## 4. lista_descuentos
Lista todos los descuentos existentes junto con las prendas que los tienen aplicados.  
Solo se muestran los descuentos cuyo **porcentaje sea igual al valor recibido por parámetro** (por ejemplo, `20`) o igual a `25`.  
Los resultados aparecen **ordenados por su fecha de expiración**.

## 5. lista_marcas
Muestra todas las marcas registradas junto con las prendas que pertenecen a cada una.  
Solo aparecen las marcas que cumplen **dos condiciones**:
- Que su **descripción contenga una palabra pasada por parámetro** (por ejemplo, `'Ropa'`).
- Que su **país de origen coincida con el valor recibido** (por ejemplo, `'Francia'`).

## 6. lista_prendas
Muestra todas las prendas disponibles que **no tienen ningún usuario asociado**.  
Cada prenda se muestra con su marca y posible descuento (si lo tuviera).  
Los resultados están **ordenados alfabéticamente por el nombre de la prenda**.

## 7. lista_reseñas
Muestra las **tres últimas reseñas publicadas**, incluyendo la prenda a la que pertenecen y el usuario que las realizó.  
Se ordenan por fecha **de más reciente a más antigua**.

## 8. lista_pedido_prendas
Muestra las **prendas que forman parte de un pedido específico**, según el ID del pedido que se le pase por parámetro (por ejemplo, `2`).  
Usa `prefetch_related` para optimizar la carga de las prendas asociadas.

## 9. lista_detallepedido_total
Muestra todos los detalles de los pedidos junto con su pedido y la prenda correspondiente.  
Además, calcula y muestra **la suma total del precio** de todos los detalles registrados.

## 10. inventario_minimo
Muestra todas las prendas cuyo **stock disponible sea menor o igual al número pasado por parámetro** (por ejemplo, `40`).  
Se obtiene la información directamente mediante una consulta **RAW SQL**, uniendo los modelos `Inventario` y `Prenda`.

---

## Uso de Template Tags en el Proyecto

Para cumplir el objetivo de usar **al menos 5 template tags diferentes**, se han utilizado los siguientes HTML en distintas páginas del proyecto:

| HTML                        | Template Tags Usados                | Descripción                                               |
|------------------------------|-----------------------------------|-----------------------------------------------------------|
| `inventario_minimo.html`     | `if-else`                         | Muestra inventarios con stock menor o igual a un mínimo. |
| `lista_pedido_prendas.html`  | `if-else`                         | Lista las prendas de un pedido, mostrando mensaje si no hay prendas. |
| `lista_prendas.html`          | `if-else`                         | Muestra prendas sin usuarios asignados, con mensaje si la lista está vacía. |
| `lista_reseña.html`           | `if-else`                         | Muestra las últimas reseñas publicadas, con mensaje si no hay reseñas. |
| `lista_cesta.html`            | `for ... empty`                    | Muestra los elementos de la cesta de usuario, mostrando un mensaje si está vacía. |

Con esto, se cumplen los requisitos de usar **5 template tags diferentes** (`if-else`, `for ... empty`) en el proyecto, aplicados en distintas páginas para manejar condiciones y listas vacías.
