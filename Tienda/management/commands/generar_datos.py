# Tienda/management/commands/generar_datos.py
from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal
from Tienda.models import (
    Usuario, PerfilUsuario, Marca, Descuento, Prenda,
    Inventario, Pedido, DetallePedido, Reseña, Cesta
)

class Command(BaseCommand):
    help = 'Genera 10 registros aleatorios para cada modelo usando Faker'

    def handle(self, *args, **kwargs):
        fake = Faker()
        usuarios = []
        marcas = []
        descuentos = []
        prendas = []
        pedidos = []

        for _ in range(10):
            usuario = Usuario.objects.create(
                nombre=fake.name(),
                identificador=fake.unique.random_int(min=1000, max=9999),
                fecha_nacimiento=fake.date_of_birth(),
                correo_electronico=fake.unique.email()
            )
            PerfilUsuario.objects.create(
                usuario=usuario,
                bio=fake.text(max_nb_chars=200),
                direccion=fake.address(),
                telefono=fake.phone_number(),
                sitio_web=fake.url()
            )
            usuarios.append(usuario)

        for _ in range(10):
            marca = Marca.objects.create(
                nombre=fake.unique.company(),
                pais_origen=fake.country(),
                descripcion=fake.text(max_nb_chars=200),
                año_fundacion=int(fake.year())
            )
            marcas.append(marca)

        for _ in range(10):
            descuento = Descuento.objects.create(
                codigo=fake.unique.bothify(text='DESC###'),
                porcentaje=Decimal(random.uniform(5, 50)).quantize(Decimal('0.01')),
                activo=random.choice([True, False]),
                fecha_expiracion=fake.date_this_year()
            )
            descuentos.append(descuento)

        tallas = ['XS','S','M','L','XL','XXL']
        for _ in range(10):
            prenda = Prenda.objects.create(
                nombre=fake.word().title(),
                descripcion=fake.text(max_nb_chars=100),
                talla=random.choice(tallas),
                color=fake.color_name(),
                precio=Decimal(random.uniform(10, 200)).quantize(Decimal('0.01')),
                marca=random.choice(marcas),
                descuento=random.choice(descuentos + [None])
            )
            prenda.usuarios.set(random.sample(usuarios, k=random.randint(1, len(usuarios))))
            prendas.append(prenda)

        for prenda in prendas:
            Inventario.objects.create(
                prenda=prenda,
                cantidad_disponible=random.randint(0, 50),
                ubicacion_almacen=fake.city(),
                stock_minimo=random.randint(1, 5),
                stock_maximo=random.randint(20, 100)
            )

        estados = ['PEND','PROC','ENV','ENT']
        for _ in range(10):
            pedido_usuario = random.choice(usuarios)
            pedido = Pedido.objects.create(
                usuario=pedido_usuario,
                total=0,
                estado=random.choice(estados),
                direccion_envio=fake.address()
            )

            pedido_prendas = random.sample(prendas, k=random.randint(1, 3))
            total = Decimal('0.0')
            for prenda in pedido_prendas:
                cantidad = random.randint(1, 5)
                DetallePedido.objects.create(
                    pedido=pedido,
                    prenda=prenda,
                    cantidad=cantidad,
                    precio=prenda.precio
                )
                total += prenda.precio * cantidad
            pedido.total = total
            pedido.save()
            pedidos.append(pedido)

        for _ in range(10):
            prenda = random.choice(prendas)
            reseña = Reseña.objects.create(
                prenda=prenda,
                calificacion=random.randint(1, 5),
                comentario=fake.text(max_nb_chars=200),
                recomendado=random.choice([True, False])
            )
            reseña.usuarios.set(random.sample(usuarios, k=random.randint(1, len(usuarios))))

            cesta = Cesta.objects.create(
                usuario=usuario,
                activo=random.choice([True, False]),
                objetos_en_cesta=0,
                precio=0
            )
            cesta_prendas = random.sample(prendas, k=random.randint(1, 5))
            cesta.prenda.set(cesta_prendas)
            total = sum([p.precio for p in cesta_prendas])
            cesta.precio = total
            cesta.objetos_en_cesta = len(cesta_prendas)
            cesta.save()

        self.stdout.write(self.style.SUCCESS("Se han generado los datos correctamente!"))
