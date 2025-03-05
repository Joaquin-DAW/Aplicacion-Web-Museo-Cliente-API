# Aplicacion-Web-Museo-Cliente-API

Muchas gracias por haber descargado mi aplicación, esta es la versión de cliente, recuerda que tambien necesitas la versión servidor API para poder desplegar ambas y que esta aplicación cliente reciba los datos del servidor. Si no sabes donde esta busca en el mismo perfil de github que te ha descargado este repositorio, se lla "Aplicacion-Web--Museo".

Una vez tengas los dos repositorios listos vamos a empezar a preparar el de servidor.

1.- Primer paso con el servidor, realizar la instalación de los requirements.txt, para ello nos vamos hasta la carpeta Museo (usando cd) y una vez aquí ejecutamos el comando: pip install -r requirements.txt. Con esto tendremos instalado python.

2.- En la misma carpeta de Museo vamos a crear el enterono virtual con python, para ello ejecutamos el comando: python3 -m venv myvenv en la terminal. Una vez creado podremos activarlo con el comando: source myvenv/bin/activate 
Esto hara que nos aparezca un (myven) al principio de cada línea del terminal, indicando que esta activo.

Como en esta carpeta ya se pasa el mysite configurado no hace falta que se cree.

3.- Arrancamos el servidor, si ejecutamos el comando python manage.py runserver, arrancaremos nuestro servidor, si quisiera arrancarlo por una ruta en concreto se lo especificariamos añadiendosela detras del propio comando, por ejemplo: python manage.py runserver 0.0.0.0:8080. Por defecto la ruta será la 127.0.0.1:8000

4.- Vamos a volver a realizar el pip install -r requirements.txt y al acabar veremos que nos da error si intentamos levantar nuestro servidor, esto se debe a que no tenemos configurado el .env en nuestro servidor, vamos a ello. Nos creamos el archivo en la misma carpeta que Museo y tomamos como referencia el .env.plantilla para saber que debe tener.

Pero tenemos un problema, necesitamos levantar el servidor para poder dar un token de verdad a nuestro servidor, así que hagamos un pequeño apaño, en el archivo .env donde pone "SECRET_KEY=" le pondremos un codigo falso, pondremos literalmetne cualquier cosa, lo mejor una sucesicón de letras aleatorias, esto obviamente no nos será útil en el futuro, pero para salir del paso nos sirve. Si guardamos y corremos nuestro servidor veremos como ahora si que nos deja.

5.- Vemos que tenemos migraciones que no se han aplicado, vamos a hacer que se apliquen usando un comando python manage.py migrate. Bien si ahora volemos a levantar el servidor todo deberia estar bien.

6.- Vamos a gestionar ahora la creacion de un token valido, para ello nos vamos a la pagina de administrador de Django. Para ello accedemos a esta url: http://127.0.0.1:8000/admin 

Veremos que nos sale un formulario de login, podemos hacer dos cosas, crear un super ususario con este comando: python manage.py createsuperuser y usar las credenciales que le hemos dado para acceder o cargar el fixtures de nuestro proyecto que ya incluye un super usuario admin con contraseña admin. Así se hace un loaddata: python manage.py loaddata appmuseo/fixtures/datosmuseo.json esto tambien cargaría todos los demas datos que tenemos para esta aplicacion, algunos datos de modelos, usuarios, grupos y permisos.

![Configuración](images/GestionarToken.PNG)

7.- Una vez hayamos accedido con un super usuario vamos a configurar el token. Para ello accedemos a esta url: http://127.0.0.1:8000/oauth2/applications/  Puede cambiar dependiendo de en que puerto tengas abierta la aplicación. Una vez accedamos a esta pagina deberemos rellenarla de una forma similar a esta:



4.- Ahora vamos a hace run paso un poco opcional, pasar los datos básicoas que tengo en el fixtures. Esto solo son datos de los modelos para que se vea algo en ellos, permisos y algunos usuarios, todo esto lo puedes hacer tú desde cero e incluso crear nuevos modelos o cambiar alguno (recuerda hacer el python manage.py makemigrations y el python manage.py migrate si cambias algo de los modelos). 

Si quiers tener los mismos datos que el fixture solo debereas hacer un comando muy simple: python manage.py loaddata appmuseo/fixtures/datosmuseo.json







# 📜 Gestión de Permisos en la API

Este documento detalla los permisos de acceso para cada tipo de usuario en la API del Museo.

## 👤 Tipos de usuarios
- **Público (No autenticado):** No ha iniciado sesión.
- **Visitante:** Usuario registrado con acceso a entradas y visitas guiadas.
- **Responsable:** Usuario con permisos avanzados para gestionar museos y otros elementos.

## 🔓 Permisos de acceso

### 📌 Museos
| Acción               | Público (No autenticado) | Visitante | Responsable |
|----------------------|------------------------|-----------|------------|
| Ver lista de Museos | ✅ Sí                   | ✅ Sí      | ✅ Sí       |
| Buscar Museos       | ✅ Sí                   | ✅ Sí      | ✅ Sí       |
| Crear un Museo      | ❌ No                   | ❌ No      | ✅ Sí       |
| Editar un Museo     | ❌ No                   | ❌ No      | ✅ Sí       |
| Eliminar un Museo   | ❌ No                   | ❌ No      | ✅ Sí       |

### 📌 Exposiciones
| Acción                   | Público (No autenticado) | Visitante | Responsable |
|--------------------------|------------------------|-----------|------------|
| Ver lista de Exposiciones | ✅ Sí                  | ✅ Sí      | ✅ Sí       |
| Buscar Exposiciones      | ✅ Sí                  | ✅ Sí      | ✅ Sí       |
| Crear una Exposición     | ❌ No                  | ❌ No      | ✅ Sí       |
| Editar una Exposición    | ❌ No                  | ❌ No      | ✅ Sí       |
| Eliminar una Exposición  | ❌ No                  | ❌ No      | ✅ Sí       |

### 📌 Obras de arte
| Acción            | Público (No autenticado) | Visitante | Responsable |
|-------------------|------------------------|-----------|------------|
| Ver lista de Obras | ✅ Sí                  | ✅ Sí      | ✅ Sí       |
| Crear una Obra    | ❌ No                  | ❌ No      | ✅ Sí       |
| Editar una Obra   | ❌ No                  | ❌ No      | ✅ Sí       |
| Eliminar una Obra | ❌ No                  | ❌ No      | ✅ Sí       |

### 📌 Artistas
| Acción            | Público (No autenticado) | Visitante | Responsable |
|-------------------|------------------------|-----------|------------|
| Ver lista de Artistas | ✅ Sí               | ✅ Sí      | ✅ Sí       |
| Crear un Artista  | ❌ No                  | ❌ No      | ✅ Sí       |
| Editar un Artista | ❌ No                  | ❌ No      | ✅ Sí       |
| Eliminar un Artista | ❌ No                | ❌ No      | ✅ Sí       |

### 📌 Tienda y productos
| Acción               | Público (No autenticado) | Visitante | Responsable |
|----------------------|------------------------|-----------|------------|
| Ver lista de productos | ✅ Sí               | ✅ Sí      | ✅ Sí       |
| Crear un Producto   | ❌ No                  | ❌ No      | ✅ Sí       |
| Editar un Producto  | ❌ No                  | ❌ No      | ✅ Sí       |
| Eliminar un Producto | ❌ No                 | ❌ No      | ✅ Sí       |
| Crear una Tienda    | ❌ No                  | ❌ No      | ✅ Sí       |
| Editar una Tienda   | ❌ No                  | ❌ No      | ✅ Sí       |
| Eliminar una Tienda | ❌ No                  | ❌ No      | ✅ Sí       |

### 📌 Entradas y visitas guiadas
| Acción                  | Público (No autenticado) | Visitante | Responsable |
|-------------------------|------------------------|-----------|------------|
| Comprar una Entrada     | ❌ No                  | ✅ Sí      | ✅ Sí       |
| Ver mis Entradas        | ❌ No                  | ✅ Sí      | ✅ Sí       |
| Editar una Entrada      | ❌ No                  | ✅ Sí      | ✅ Sí       |
| Eliminar una Entrada    | ❌ No                  | ✅ Sí      | ✅ Sí       |
| Reservar una Visita Guiada | ❌ No               | ✅ Sí      | ✅ Sí       |
| Editar una Visita Guiada | ❌ No                | ✅ Sí      | ✅ Sí       |
| Eliminar una Visita Guiada | ❌ No              | ✅ Sí      | ✅ Sí       |

### 📌 Guías de visitas
| Acción            | Público (No autenticado) | Visitante | Responsable |
|-------------------|------------------------|-----------|------------|
| Crear un Guía    | ❌ No                   | ❌ No      | ✅ Sí       |
| Editar un Guía   | ❌ No                   | ❌ No      | ✅ Sí       |
| Eliminar un Guía | ❌ No                   | ❌ No      | ✅ Sí       |
