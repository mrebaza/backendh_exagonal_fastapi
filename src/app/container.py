from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pika

from ..config import settings
from ..contexts.users.infrastructure.adapters.db_repository import DBUserRepository
from ..contexts.users.infrastructure.adapters.mq_command_bus import RabbitMQCommandBus
from ..contexts.users.application.use_cases_command import UserCreator


class AppContainer(containers.DeclarativeContainer):
    """Contenedor principal de Inyección de Dependencias."""
    wiring_config = containers.WiringConfiguration(
        modules=[
            ".main",
            "..contexts.users.infrastructure.api.router",
        ]
    )

    # Configuración
    config = providers.Configuration()
    config.from_dict(settings.model_dump())

    # Base de Datos (Adaptador de persistencia)
    db_engine = providers.Singleton(create_engine, url=config.DATABASE_URL)
    db_session_factory = providers.Factory(sessionmaker, bind=db_engine, autocommit=False, autoflush=False)

    user_repository = providers.Factory(DBUserRepository, db_session_factory=db_session_factory)

    # RabbitMQ (Adaptador de mensajería)
    rabbitmq_connection_params = providers.Singleton(
        pika.ConnectionParameters, host=config.RABBITM_HOST
    )
    
    rabbitmq_connection = providers.Singleton(pika.BlockingConnection, rabbitmq_connection_params)
    command_bus = providers.Singleton(
        RabbitMQCommandBus,
        host=config.RABBITMQ_HOST,
        user=config.RABBITMQ_USER,
        password=config.RABBITMQ_PASS,
    )

    # Casos de Uso
    user_creator = providers.Factory(UserCreator, user_repository=user_repository)