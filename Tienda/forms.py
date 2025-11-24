from django import forms
from django.forms import ModelForm
from .models import * 

class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre","identificador","fecha_nacimiento","correo_electronico"]
        labels = {
            "nombre":("Nombre de Usuario"),
            "identificador":("identificador"),
            "fecha_nacimiento":("Fecha de nacimiento"),
            "correo_electronico":("Correo Electronico"),
        }
        helps_text ={
            "nombre":("200 caracteres como máximo"),
        }

    def clean(self):
      
       #Validamos con el modelo actual
       super().clean()
      
       #Obtenemos los campos
       nombre_usuario = self.cleaned_data.get('nombre')
       correo_electronico = self.cleaned_data.get('correo_electronico')


       #Comprobamos
       if len(nombre_usuario) < 3:
           self.add_error('nombre_usuario','El nombre debe tener al menos 3 caracteres.')
      
       if len(correo_electronico) < 6:
           self.add_error('correo_electronico','El correo electronico debe tener al menos 6 caracteres.')


       #Siempre devolvemos el conjunto de datos.
       return self.cleaned_data