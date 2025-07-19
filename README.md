# Proyecto Backend: Arquitectura Hexagonal & CQRS

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green)
![Docker](https://img.shields.io/badge/Docker-20.10-blue)
![Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)

Este proyecto es una implementación robusta de una API REST construida con **Arquitectura Hexagonal**, **CQRS** y **Contextos Delimitados**. Proporciona una base escalable y modular para el desarrollo backend, utilizando patrones de diseño modernos y herramientas como FastAPI, SQLAlchemy, RabbitMQ y Docker.

## Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Decisiones Arquitectónicas](#decisiones-arquitectónicas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Prerrequisitos](#prerrequisitos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Ejecutar el Proyecto](#ejecutar-el-proyecto)
- [Ejecutar Pruebas](#ejecutar-pruebas)
- [Endpoints de la API](#endpoints-de-la-api)
  - [Contexto de Usuarios](#contexto-de-usuarios)
- [Variables de Entorno](#variables-de-entorno)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Descripción del Proyecto

Este proyecto sirve como una implementación de referencia para un sistema backend diseñado con:

- **Arquitectura Hexagonal**: Aísla la lógica de negocio de las dependencias externas, permitiendo un desarrollo agnóstico a la tecnología.
- **CQRS (Segregación de Responsabilidad de Comandos y Consultas)**: Separa las operaciones de escritura y lectura para optimizar el rendimiento y la escalabilidad.
- **Contextos Delimitados**: Organiza el código por dominios de negocio (`users`, `auth`) para mejorar la modularidad y la colaboración en equipo.

La aplicación utiliza **FastAPI** para la capa de API, **SQLAlchemy** para interacciones con la base de datos, **RabbitMQ** para el procesamiento asíncrono de comandos y **Docker** para un despliegue en contenedores.

## Decisiones Arquitectónicas

- **Arquitectura Hexagonal**: Garantiza que la lógica de negocio sea independiente de frameworks y bases de datos, permitiendo cambios de tecnología sin problemas. [cite: 6]
- **CQRS**: Separa los comandos (operaciones de escritura) de las consultas (operaciones de lectura) para optimizar el rendimiento y la escalabilidad. Los comandos se procesan de forma asíncrona mediante **RabbitMQ** para mayor resiliencia. [cite: 7, 59]
- **Contextos Delimitados**: Organiza el código por dominios de negocio (`users`, `auth`) en lugar de capas técnicas, promoviendo modularidad y desarrollo paralelo. [cite: 9, 54]
- **Inyección de Dependencias**: Utiliza `dependency-injector` para desacoplar componentes, facilitar pruebas y simplificar la configuración.

## Estructura del Proyecto

El código está organizado en **Contextos Delimitados** para garantizar alta cohesión y bajo acoplamiento. [cite: 9]

### Estructura de Directorios Propuesta

Esta es la estructura que construiremos. Refleja todos los principios anteriores.

```
/backend-project
|-- docker-compose.yml         # Orquesta nuestros servicios (API, Worker, DB, RabbitMQ)
|-- .env                       # Variables de entorno (secretos, configuraciones)
|-- /src                       # Todo nuestro código fuente
|   |-- /app                   # Configuración de FastAPI y contenedores de inyección de dependencias
|   |   |-- __init__.py
|   |   |-- container.py       # Contenedor de Inyección de Dependencias
|   |   `-- main.py            # Punto de entrada de la aplicación FastAPI
|   |
|   |-- /contexts              # Aquí residen nuestros Contextos Delimitados
|   |   |-- /shared            # Módulos compartidos (Value Objects, etc.)
|   |   |
|   |   `-- /users             # Contexto de Usuarios
|   |       |-- /domain          # Lógica de negocio pura, sin dependencias externas
|   |       |   |-- entities.py    # El Agregado User
|   |       |   `-- repository.py  # El Puerto (interfaz) del repositorio
|   |       |
|   |       |-- /application     # Orquesta el dominio (Casos de Uso)
|   |       |   |-- commands.py    # DTOs para comandos (ej. CreateUserCommand)
|   |       |   |-- queries.py     # DTOs para consultas (ej. UserDTO)
|   |       |   `-- use_cases.py   # Lógica de los casos de uso
|   |       |
|   |       `-- /infrastructure  # Implementaciones concretas (Adaptadores)
|   |           |-- /adapters      # Implementaciones de los puertos
|   |           |   |-- db_repository.py  # Adaptador para SQLAlchemy
|   |           |   `-- mq_command_bus.py # Adaptador para publicar en RabbitMQ
|   |           |-- /api
|   |           |   `-- router.py     # Endpoints de FastAPI para usuarios
|   |           `-- /persistence
|   |               `-- user_model.py # Modelo de SQLAlchemy
|   |
|   |-- /worker                  # El consumidor de RabbitMQ
|   |   |-- __init__.py
|   |   |-- container.py       # Contenedor de inyección de dependencias para el worker
|   |   `-- main.py            # Lógica para consumir comandos
|   |
|   `-- /config.py             # Carga de configuración (Pydantic)
|
|-- /tests                     # Pruebas unitarias y de integración
|   `-- /contexts
|       `-- /users
|           |-- /domain
|           |   `-- test_entities.py
|           `-- /application
|               `-- test_use_cases.py
|
`-- README.md                  # Documentación del proyecto
```

## Prerrequisitos

- **Python**: 3.9 o superior
- **Docker**: 20.10 o superior
- **Docker Compose**: 1.29 o superior
- **Git**: Para clonar el repositorio

## Instalación y Configuración

1. **Clonar el Repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd <directorio-del-repositorio>
   ```

2. **Configurar Variables de Entorno**:
   Copia el archivo `.env.example` a `.env` y completa los valores requeridos:
   ```bash
   cp .env.example .env
   ```

3. **Instalar Dependencias** (opcional, para desarrollo local sin Docker):
   ```bash
   pip install -r requirements.txt
   ```

## Ejecutar el Proyecto

Inicia los servicios usando Docker Compose, que incluye la API (puerto 8000), el worker, la base de datos PostgreSQL y RabbitMQ:

```bash
docker-compose up --build
```

Accede a la API en `http://localhost:8000`. Usa la documentación interactiva de la API en `http://localhost:8000/docs`.

## Ejecutar Pruebas

Ejecuta el conjunto de pruebas usando pytest:

```bash
pytest
```

Ejecuta para ver la cobertura usando pytest:

```bash
pytest --cov=src --cov-report=term-missing

```

Ejecuta para ver la cobertura en HTML:

```bash
pytest --cov=src --cov-report=html

```

Luego abrir el archivo en la siguiente ruta:

 - htmlcov/index.html

Asegúrate de que los servicios de base de datos y RabbitMQ estén activos antes de ejecutar las pruebas.

## Endpoints de la API

### Contexto de Usuarios

#### `POST /users`

- **Descripción**: Crea un nuevo usuario publicando un `CreateUserCommand` en una cola de RabbitMQ para procesamiento asíncrono.
- **Cuerpo de la Solicitud**:
  ```json
  {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "una-contraseña-muy-segura"
  }
  ```
- **Respuestas**:
  - `202 Accepted`: Solicitud aceptada para procesamiento.
  - `422 Unprocessable Entity`: Cuerpo de la solicitud no válido.

#### `GET /users/{user_id}`

- **Descripción**: Obtiene los detalles de un usuario por su ID, consultando directamente la base de datos (Consulta CQRS). [cite: 25, 37]
- **Parámetro de Ruta**:
  - `user_id` (UUID): Identificador único del usuario.
- **Respuestas**:
  - `200 OK`:
    ```json
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "John Doe",
      "email": "john.doe@example.com"
    }
    ```
  - `404 Not Found`: Usuario no encontrado.

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```ini
# Base de Datos PostgreSQL
POSTGRES_USER=miusuario
POSTGRES_PASSWORD=micontraseña
POSTGRES_DB=mibasededatos

# RabbitMQ
RABBITMQ_USER=guest
RABBITMQ_PASS=guest

# URLs de conexión (usadas por la aplicación y el worker en Docker)
DATABASE_URL=postgresql://miusuario:micontraseña@db:5432/mibasededatos
RABBITMQ_HOST=rabbitmq
```

## Contribuir

¡Las contribuciones son bienvenidas! Sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad (`git checkout -b feature/tu-funcionalidad`).
3. Confirma tus cambios (`git commit -m "Añade tu funcionalidad"`).
4. Sube la rama (`git push origin feature/tu-funcionalidad`).
5. Abre un Pull Request.

Asegúrate de que tu código siga los estándares del proyecto e incluya pruebas.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.