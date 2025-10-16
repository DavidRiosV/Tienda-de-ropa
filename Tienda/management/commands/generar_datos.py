# Tienda/management/commands/generar_datos.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Genera datos de prueba con Faker'

    def handle(self, *args, **kwargs):
        # aquí va tu código de Faker
        self.stdout.write(self.style.SUCCESS('Datos generados correctamente!'))
