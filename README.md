# Aplicacion-Web-Museo-Cliente-API

Muchas gracias por haber descargado mi aplicación, esta es la versión de cliente, recuerda que tambien necesitas la versión servidor API para poder desplegar ambas y que esta aplicación cliente reciba los datos del servidor. Si no sabes donde esta busca en el mismo perfil de github que te ha descargado este repositorio, se lla "Aplicacion-Web--Museo".



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
