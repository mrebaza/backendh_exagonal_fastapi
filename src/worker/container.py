
from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from ..config import settings
# from ..contexts.users.infrastructure.adapters.db_repository import DBUserRepository
# from ..contexts.users.application.use_cases import UserCreator

from src.contexts.users.infrastructure.adapters.mq_command_bus import RabbitMQCommandBus
from src.config import settings
from src.contexts.users.infrastructure.adapters.db_repository import DBUserRepository
# from contexts.users.application.use_cases_command import UserCreator
from src.contexts.users.application.use_cases_command import UserCreator



class WorkerContainer(containers.DeclarativeContainer):
    """
    Contenedor de Inyección de Dependencias específico para el Worker.
    Solo contiene las dependencias necesarias para procesar comandos.
    """
    # wiring_config = containers.WiringConfiguration(modules=[".main"])
    wiring_config = containers.WiringConfiguration(modules=["src.worker.main"])


    # Configuración
    config = providers.Configuration()
    config.from_dict(settings.model_dump())


    # Base de Datos
    db_engine = providers.Singleton(create_engine, url=config.DATABASE_URL)
    db_session_factory = providers.Factory(
        sessionmaker, 
        bind=db_engine, 
        autocommit=False, 
        autoflush=False
    )

    # Repositorios (Adaptadores de persistencia)
    user_repository = providers.Factory(
        DBUserRepository, 
        db_session_factory=db_session_factory
    )
        
    # Bus de Comandos (RabbitMQ)
    # command_bus = providers.Singleton(RabbitMQCommandBus, host=settings.RABBITMQ
    command_bus = providers.Singleton(RabbitMQCommandBus, 
                                      host=config.RABBITMQ_HOST(), 
                                      user=config.RABBITMQ_USER(), 
                                      password=config.RABBITMQ_PASS())


    # Casos de Uso (Lógica de aplicación)
    user_creator = providers.Factory(
        UserCreator, 
        user_repository=user_repository,
        command_bus=command_bus
    )

    
