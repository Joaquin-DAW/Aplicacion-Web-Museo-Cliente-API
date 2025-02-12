from django import forms
from .models import *
import requests
from datetime import date
import datetime
from .helper import helper

class BusquedaMuseoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True, label="Buscar Museo", max_length=150)
    
class BusquedaAvanzadaMuseoForm(forms.Form):
    nombre_descripcion = forms.CharField(
        required=False, 
        label="Escriba el nombre o la descripción del museo",
        widget=forms.TextInput(attrs={"placeholder": "Nombre o descripción del museo"})
    )
    ubicacion = forms.CharField(
        required=False, 
        label="Escriba la ubicación del museo",
        widget=forms.TextInput(attrs={"placeholder": "Ubicación del museo"})
    )
    fecha_desde = forms.DateField(
        label="Fecha Desde",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    fecha_hasta = forms.DateField(
        label="Fecha Hasta",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    

class MuseoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre del Museo",
        required=True,
        max_length=200,
        help_text="Máximo 200 caracteres."
    )

    ubicacion = forms.CharField(
        label="Ubicación",
        required=False,
        max_length=200,
        help_text="Proporcione la dirección o ubicación del museo.",
        widget=forms.TextInput(attrs={"placeholder": "Ejemplo: Calle 123, Ciudad, País"})
    )

    fecha_fundacion = forms.DateField(
        label="Fecha de Fundación",
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(years=range(1800, datetime.date.today().year + 1)),
        help_text="Seleccione la fecha en la que se fundó el museo."
    )

    descripcion = forms.CharField(
        label="Descripción",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Añade una breve descripción del museo."}),
        help_text="Breve descripción del museo. Mínimo 10 caracteres."
    )

    imagen = forms.FileField(
        label="Imagen del Museo",
        required=False,
        help_text="Opcional: puedes subir una imagen del museo."
    )

    def clean(self):
        """ Validaciones personalizadas """
        cleaned_data = super().clean()

        nombre = cleaned_data.get("nombre")
        ubicacion = cleaned_data.get("ubicacion", "")
        fecha_fundacion = cleaned_data.get("fecha_fundacion")
        descripcion = cleaned_data.get("descripcion", "")

        # Validar que el nombre no supere 200 caracteres
        if len(nombre) > 200:
            self.add_error("nombre", "El nombre no puede superar los 200 caracteres.")

        # Validar que la ubicación tenga al menos 10 caracteres si se proporciona
        if ubicacion and len(ubicacion) < 10:
            self.add_error("ubicacion", "La ubicación debe tener al menos 10 caracteres.")

        # Validar que la fecha de fundación no sea mayor a hoy
        if fecha_fundacion and fecha_fundacion > datetime.date.today():
            self.add_error("fecha_fundacion", "La fecha de fundación no puede ser futura.")

        # Validar que la descripción tenga al menos 10 caracteres si se proporciona
        if descripcion and len(descripcion) < 10:
            self.add_error("descripcion", "La descripción debe tener al menos 10 caracteres.")

        return cleaned_data

    
class BusquedaAvanzadaObraForm(forms.Form):
    titulo = forms.CharField(
        required=False,
        label="Título de la obra",
        widget=forms.TextInput(attrs={"placeholder": "Título de la obra"})
    )
    fecha_creacion_desde = forms.DateField(
        label="Fecha de creación desde",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    fecha_creacion_hasta = forms.DateField(
        label="Fecha de creación hasta",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    tipo = forms.ChoiceField(
        choices=[('', 'Seleccione un tipo'), ('pintura', 'Pintura'), ('escultura', 'Escultura')],
        required=False,
        label="Tipo"
    )
    exposicion = forms.ChoiceField(
        choices=[],  # Inicialmente vacío
        required=False,
        label="Exposición"
    )
    artista = forms.ChoiceField(
        choices=[],  # Inicialmente vacío
        required=False,
        label="Artista"
    )

    def __init__(self, *args, **kwargs):
        super(BusquedaAvanzadaObraForm, self).__init__(*args, **kwargs)
        # Cargar las exposiciones vía API
        try:
            response_expo = requests.get("http://127.0.0.1:8000/api/v1/exposiciones/")
            if response_expo.status_code == 200:
                data_expo = response_expo.json()
                # Suponiendo que cada objeto tiene 'id' y 'titulo'
                self.fields['exposicion'].choices = [('', 'Seleccione una exposición')] + [
                    (expo['id'], expo['titulo']) for expo in data_expo
                ]
            else:
                self.fields['exposicion'].choices = [('', 'No hay exposiciones')]
        except Exception as e:
            self.fields['exposicion'].choices = [('', 'Error al cargar exposiciones')]

        # Cargar los artistas vía API
        try:
            response_artista = requests.get("http://127.0.0.1:8000/api/v1/artistas/")
            if response_artista.status_code == 200:
                data_artista = response_artista.json()
                # Suponiendo que cada objeto tiene 'id' y 'nombre_completo'
                self.fields['artista'].choices = [('', 'Seleccione un artista')] + [
                    (art['id'], art['nombre_completo']) for art in data_artista
                ]
            else:
                self.fields['artista'].choices = [('', 'No hay artistas')]
        except Exception as e:
            self.fields['artista'].choices = [('', 'Error al cargar artistas')]
            

class BusquedaAvanzadaExposicionForm(forms.Form):
    titulo = forms.CharField(
        required=False,
        label="Título de la exposición",
        widget=forms.TextInput(attrs={"placeholder": "Título de la exposición"})
    )
    descripcion = forms.CharField(
        required=False,
        label="Descripción de la exposición",
        widget=forms.TextInput(attrs={"placeholder": "Descripción de la exposición"})
    )
    fecha_desde = forms.DateField(
        label="Fecha de inicio desde",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    fecha_hasta = forms.DateField(
        label="Fecha de inicio hasta",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
    )
    museo = forms.ChoiceField(
        choices=[],  # Se llenará dinámicamente
        required=False,
        label="Museo"
    )

    def __init__(self, *args, **kwargs):
        super(BusquedaAvanzadaExposicionForm, self).__init__(*args, **kwargs)
        # Cargar museos vía API
        try:
            response_museo = requests.get("http://127.0.0.1:8000/api/v1/museos/")
            if response_museo.status_code == 200:
                data_museo = response_museo.json()
                # Se asume que cada objeto tiene 'id' y 'nombre'
                self.fields['museo'].choices = [('', 'Seleccione un museo')] + [
                    (m['id'], m['nombre']) for m in data_museo
                ]
            else:
                self.fields['museo'].choices = [('', 'No hay museos')]
        except Exception as e:
            self.fields['museo'].choices = [('', 'Error al cargar museos')]
            
            
class BusquedaAvanzadaEntradaForm(forms.Form):
    codigo = forms.CharField(
        required=False,
        label="Código de la entrada",
        widget=forms.TextInput(attrs={"placeholder": "Código de la entrada"})
    )
    precio_min = forms.DecimalField(
        required=False,
        label="Precio mínimo",
        decimal_places=2,
        max_digits=6,
        widget=forms.NumberInput(attrs={"placeholder": "Precio mínimo"})
    )
    precio_max = forms.DecimalField(
        required=False,
        label="Precio máximo",
        decimal_places=2,
        max_digits=6,
        widget=forms.NumberInput(attrs={"placeholder": "Precio máximo"})
    )
    tipo = forms.ChoiceField(
        choices=[('', 'Seleccione un tipo'), ('adulto', 'Adulto'), ('nino', 'Niño')],
        required=False,
        label="Tipo"
    )
    visitante = forms.ChoiceField(
        choices=[],  # Se llenará dinámicamente
        required=False,
        label="Visitante"
    )

    def __init__(self, *args, **kwargs):
        super(BusquedaAvanzadaEntradaForm, self).__init__(*args, **kwargs)
        # Cargar visitantes vía API
        try:
            response_visitante = requests.get("http://127.0.0.1:8000/api/v1/visitantes/")
            if response_visitante.status_code == 200:
                data_visitante = response_visitante.json()
                self.fields['visitante'].choices = [('', 'Seleccione un visitante')] + [
                    (v['id'], v['nombre']) for v in data_visitante
                ]
            else:
                self.fields['visitante'].choices = [('', 'No hay visitantes disponibles')]
        except Exception:
            self.fields['visitante'].choices = [('', 'Error al cargar visitantes')]
