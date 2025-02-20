from django import forms
from .models import *
import requests
from datetime import date
import datetime
import environ

env = environ.Env()
environ.Env.read_env()

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
    
# Crear Museo (POST)
class MuseoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre del Museo",
        required=True,
        max_length=200,
        help_text="Nombre del museo (máximo 200 caracteres)."
    )
    ubicacion = forms.CharField(
        label="Ubicación del Museo",
        required=True,
        min_length=10,
        help_text="Proporcione la dirección o ubicación del museo."
    )
    fecha_fundacion = forms.DateField(
        label="Fecha de Fundación",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        help_text="Fecha en que se fundó el museo."
    )
    descripcion = forms.CharField(
        label="Descripción",
        required=True,
        min_length=10,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Añade una breve descripción del museo."}),
        help_text="Breve descripción del museo."
    )

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if len(nombre) > 200:
            raise forms.ValidationError("El nombre no puede superar los 200 caracteres.")
        return nombre

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get("ubicacion")
        if len(ubicacion) < 10:
            raise forms.ValidationError("La ubicación debe tener al menos 10 caracteres.")
        return ubicacion

    def clean_fecha_fundacion(self):
        fecha_fundacion = self.cleaned_data.get("fecha_fundacion")
        if fecha_fundacion > date.today():
            raise forms.ValidationError("La fecha de fundación no puede ser en el futuro.")
        return fecha_fundacion

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion")
        if len(descripcion) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return descripcion

    def enviar_datos(self):
        """
        Envía los datos a la API para crear un nuevo museo.
        """
        url = "http://127.0.0.1:8000/api/v1/museos/"  # Ajustar la URL según corresponda
        datos = {
            "nombre": self.cleaned_data["nombre"],
            "ubicacion": self.cleaned_data["ubicacion"],
            "fecha_fundacion": self.cleaned_data["fecha_fundacion"].strftime("%Y-%m-%d"),
            "descripcion": self.cleaned_data["descripcion"],
        }
        
        try:
            respuesta = requests.post(url, json=datos)
            return respuesta.json() if respuesta.status_code == 201 else respuesta.text
        except requests.exceptions.RequestException as e:
            return {"error": "No se pudo conectar con la API", "detalles": str(e)}

    
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
            
# POST Exposicion
class ExposicionForm(forms.Form):
    titulo = forms.CharField(
        label="Título de la Exposición",
        required=True,
        max_length=150,
        help_text="Máximo 150 caracteres."
    )
    fecha_inicio = forms.DateField(
        label="Fecha de Inicio",
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        help_text="Fecha en que comienza la exposición."
    )
    fecha_fin = forms.DateField(
        label="Fecha de Fin",
        required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        help_text="Fecha en que termina la exposición (opcional)."
    )
    descripcion = forms.CharField(
        label="Descripción",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Añade una breve descripción."}),
        help_text="Breve descripción de la exposición.",
        initial=""
    )
    capacidad = forms.IntegerField(
        label="Capacidad",
        required=True,
        min_value=1,
        help_text="Capacidad máxima de la exposición."
    )
    museo = forms.ChoiceField(
        label="Museo",
        required=True,
        choices=[],
        help_text="Seleccione el museo al que pertenece esta exposición."
    )

    def __init__(self, *args, **kwargs):
        super(ExposicionForm, self).__init__(*args, **kwargs)
        self.fields['museo'].choices = self.obtener_museos()

    def obtener_museos(self):
        """
        Obtiene la lista de museos disponibles desde la API.
        """

        headers = {
        "Authorization": f"Bearer {env('TOKEN_ACCESO')}",  # 🔹 Pasar el token
        "Content-Type": "application/json",
    }

        try:
            response = requests.get("http://127.0.0.1:8000/api/v1/museos", headers=headers)

            if response.status_code == 200:
                museos = response.json()
                return [(museo["id"], museo["nombre"]) for museo in museos]
            elif response.status_code == 401:
                print("⚠️ Error 401: Token de autenticación no válido o no proporcionado.")
        except requests.exceptions.RequestException as e:
            print("⚠️ Error obteniendo museos:", e)
            
            return []

    def clean_fecha_fin(self):
        """
        Valida que la fecha de fin sea mayor o igual a la fecha de inicio.
        """
        fecha_inicio = self.cleaned_data.get("fecha_inicio")
        fecha_fin = self.cleaned_data.get("fecha_fin")

        if fecha_fin and fecha_inicio and fecha_fin < fecha_inicio:
            raise forms.ValidationError("La fecha de fin debe ser posterior o igual a la fecha de inicio.")
        return fecha_fin

    def clean_titulo(self):
        """
        Valida que el título no tenga más de 150 caracteres.
        """
        titulo = self.cleaned_data.get("titulo")
        if len(titulo) > 150:
            raise forms.ValidationError("El título no puede superar los 150 caracteres.")
        return titulo


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


# Crear formulario PATCH para actualizar un museo

class MuseoEditarNombreForm(forms.Form):
    nombre = forms.CharField(
        label="Nuevo Nombre del Museo",
        required=True,
        max_length=200,
        help_text="Máximo 200 caracteres"
    )
