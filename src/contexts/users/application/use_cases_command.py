from ..domain.entities import User
from ..domain.repository import UserRepository
from .commands import CreateUserCommand

class UserCreator:
    """Caso de uso para crear un usuario."""
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository

    def handle(self, command: CreateUserCommand) -> None:
        # Validar que el usuario no exista
        if self._repository.find_by_email(command.email):
            raise ValueError("Usuario con este email ya existe")

        hashed_password = User.hash_password(command.password)
        user = User(
            # id=command.id,
            name=command.name,
            email=command.email,
            hashed_password=hashed_password
        )
        self._repository.save(user)