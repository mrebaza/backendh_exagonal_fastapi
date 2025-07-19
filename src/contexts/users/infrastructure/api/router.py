from fastapi import APIRouter, Depends, status, HTTPException
import uuid
from dependency_injector.wiring import inject, Provide

from ...application.commands import CreateUserCommand
from ...application.queries import UserDTO
from ...domain.repository import UserRepository
from .....app.container import AppContainer # Importamos el contenedor principal

router = APIRouter()

@router.post(
    "/users",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Encola un comando de creación de usuario"
)

@inject
def create_user(
    command: CreateUserCommand,
    command_bus = Depends(Provide[AppContainer.command_bus])
):
    """
    Endpoint para el COMANDO. No crea el usuario directamente,
    sino que envía el comando a RabbitMQ.
    """
    
    print("Mensaje publicado...  router.py")
    command_bus.publish("user_events", command.model_dump_json())
    
    # repository = SQLAlchemyUserRepository(db)
    # use_case = CreateUserUseCase(repository)
    # try:
    #     return use_case.execute(command)
    # except ValueError as e:
    #     raise HTTPException(status_code=422, detail=str(e))
    
    return {"message": "Creación de usuario encolada correctamente"}


@router.get(
    "/users/{user_id}",
    response_model=UserDTO,
    summary="Obtiene un usuario por ID"
)

@inject
def get_user_by_id(
    user_id: uuid.UUID,
    user_repository: UserRepository = Depends(Provide[AppContainer.user_repository]),
):
    """
    Endpoint para la CONSULTA. Lee directamente de la base de datos
    a través del repositorio.
    """
    user = user_repository.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user