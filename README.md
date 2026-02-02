The Mandalorian Rental

Este es un sistema Full-Stack que simula una plataforma de alquiler de videos bajo demanda (VOD) para la serie "The Mandalorian". El núcleo del proyecto es el uso de Redis no solo como base de datos, sino como gestor de estados temporales mediante el uso de TTL (Time To Live) para manejar reservas y alquileres.

Tecnologías Utilizadas

Backend

Python 3.12: Lenguaje principal.

Flask: Micro-framework web para la API REST.

Redis-py: Cliente para la conexión con la base de datos.

Flask-CORS: Manejo de orígenes cruzados.

Frontend

React + Vite: Entorno de desarrollo rápido para frontend.

Bootstrap 5: Estilizado de la interfaz y componentes.

Axios: Consumo de la API del backend.

SweetAlert2: Alertas visuales interactivas.

Base de Datos & Infraestructura

Redis (Alpine): Base de datos en memoria clave-valor.

Docker & Docker Compose: Orquestación de contenedores y redes.

⚙️ Lógica del Negocio (Redis)

El sistema aprovecha la funcionalidad nativa de expiración de claves de Redis (SETEX) para manejar la lógica de negocio sin necesidad de tareas programadas (cron jobs).

Estado

Descripción Técnica en Redis

Comportamiento

Disponible

La clave del episodio existe en la lista maestra, pero no existen claves de reserva ni alquiler.

El usuario puede reservar.

Reservado ⏳

Se crea una clave reserva:{id} con un TTL de 240 segundos (4 min).

El capítulo se bloquea. Si no se paga en 4 min, la clave se autodestruye y vuelve a estar disponible.

Alquilado 🔒

Se elimina la clave de reserva y se crea una clave alquiler:{id} con un TTL de 86400 segundos (24 horas).

El usuario tiene acceso confirmado por un día. Luego, expira automáticamente.

🚀 Instalación y Ejecución

Prerrequisitos

Tener Docker Desktop instalado y corriendo.

Pasos

Clonar o descargar la carpeta del proyecto.

Abrir una terminal en la raíz (Redis-The-Mandalorian).

Ejecutar el comando de construcción y levantamiento:

docker compose up --build

Esperar a que los servicios se inicien.

🖥️ Acceso a la Aplicación

Servicio

URL Local

Descripción

Frontend (Web)

http://localhost:5173

Interfaz visual para reservar y pagar.

Backend (API)

http://localhost:5000/api/episodios

JSON con el estado de los capítulos.

📡 Documentación de API (Endpoints)

El backend expone los siguientes endpoints para la gestión de capítulos:

1. Listar Episodios

Método: GET

URL: /api/episodios

Descripción: Devuelve todos los capítulos y calcula su estado actual (Disponible, Reservado o Alquilado) verificando la existencia de claves en Redis.

2. Reservar Capítulo

Método: POST

URL: /api/reservar/<id>

Descripción: Intenta reservar un capítulo.

Lógica Redis: Ejecuta SETEX reserva:<id> 240 "ocupado". Si ya existe una clave de reserva o alquiler, devuelve error 409.

3. Confirmar Pago (Alquilar)

Método: POST

URL: /api/pagar/<id>

Body: { "monto": 100 }

Descripción: Valida el monto y confirma el alquiler.

Lógica Redis:

Verifica que exista reserva:<id>.

Elimina reserva:<id>.

Crea SETEX alquiler:<id> 86400 "pagado".
