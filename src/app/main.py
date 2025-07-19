from fastapi import FastAPI
from .container import AppContainer
from ..contexts.users.infrastructure.api import router as user_router
from ..contexts.users.infrastructure.persistence.user_model import Base

def create_app() -> FastAPI:
    """
    Función de fábrica para crear la instancia de la aplicación FastAPI.
    """
    # Inicializar el contenedor de inyección de dependencias
    container = AppContainer()
    
    # Conectar los módulos que necesitan inyección de dependencias
    container.wire(modules=[__name__, "..contexts.users.infrastructure.api.router"])

    # Crear la instancia de la aplicación FastAPI
    app = FastAPI(
        title="Proyecto Backend Hexagonal & CQRS",
        description="Una base sólida para un proyecto con FastAPI, Arquitectura Hexagonal y CQRS.",
        version="0.1.0"
    )

    # Enganchar el contenedor a la aplicación para que esté disponible en las dependencias
    app.container = container

    # Incluir los routers de los diferentes contextos
    app.include_router(user_router.router, tags=["Users"], prefix="/api/v1")

    # Crear las tablas de la base de datos al iniciar la aplicación
    # En un entorno de producción real, esto se manejaría con migraciones (ej. Alembic)
    db_engine = container.db_engine()
    Base.metadata.create_all(bind=db_engine)

    return app

# Crear la aplicación
app = create_app()

@app.get("/health", tags=["Monitoring"])
def health_check():
    """Endpoint de salud para verificar que la API está funcionando."""
    return {"status": "ok"}
