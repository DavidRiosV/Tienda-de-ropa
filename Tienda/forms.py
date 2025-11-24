from django import forms
from django.forms import ModelForm
from .models import * 

#-------------------------------------------------------------------------------------------
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
    
#-------------------------------------------------------------------------------------------

class MarcaForm(ModelForm):
    class Meta:
        model = Marca
        fields = ["nombre","pais_origen","descripcion","año_fundacion"]
        labels = {
            "nombre":("Nombre de la Marca"),
            "pais_origen":("Pais de origen"),
            "descripcion":("Descripción"),
            "año_fundacion":("Año de fundación"),
        }
        helps_text ={
            "nombre":("100 caracteres como máximo"),
            "pais_origen":("100 caracteres como máximo"),
        }

    def clean(self):
      
       #Validamos con el modelo actual
       super().clean()
      
       #Obtenemos los campos
       nombre_marca = self.cleaned_data.get('nombre')
       año_fundacion = self.cleaned_data.get('año_fundacion')


       #Comprobamos
       if len(nombre_marca) < 3:
           self.add_error('nombre_marca','El nombre debe tener al menos 3 caracteres.')
      
       if int(año_fundacion) > 2026:
           self.add_error('año_fundacion','El año de origen debe ser anterior al actual.')
        
           
       #Siempre devolvemos el conjunto de datos.
       return self.cleaned_data
    
#-------------------------------------------------------------------------------------------

class DescuentoForm(ModelForm):
    class Meta:
        model = Descuento
        fields = ["codigo","porcentaje","activo","fecha_expiracion"]
        labels = {
            "codigo":("Codigo"),
            "porcentaje":("Descuento"),
            "activo":("Estado"),
            "fecha_expiracion":("Fecha de expiración"),
        }
        helps_text ={
            "codigo":("20 caracteres como máximo"),
            "porcentaje":("No puede ser mayor de 100%"),
        }

    def clean(self):
      
       #Validamos con el modelo actual
       super().clean()
      
       #Obtenemos los campos
       codigo = self.cleaned_data.get('codigo')
       porcentaje = self.cleaned_data.get('porcentaje')


       #Comprobamos
       if len(codigo) < 5:
           self.add_error('codigo','El codigo debe tener al menos 5 caracteres.')

       if float(porcentaje) > 100:
           self.add_error('porcentaje','El porcentaje no puede ser mayor de 100.')
        
           
       #Siempre devolvemos el conjunto de datos.
       return self.cleaned_data
    
#-------------------------------------------------------------------------------------------

