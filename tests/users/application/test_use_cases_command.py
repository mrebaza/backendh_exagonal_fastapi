import pytest
import uuid
from typing import Dict, Optional

from src.contexts.users.domain.entities import User
from src.contexts.users.domain.repository import UserRepository
from src.contexts.users.application.use_cases_command import UserCreator
from src.contexts.users.application.commands import CreateUserCommand

# --- Fake/Mock Implementations para las pruebas ---

class FakeUserRepository(UserRepository):
    """
    Implementación de repositorio en memoria para pruebas unitarias.
    Esto nos permite probar el caso de uso sin una base de datos real.
    """
    def __init__(self):
        self._users: Dict[uuid.UUID, User] = {}

    def save(self, user: User) -> None:
        self._users[user.id] = user

    def find_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

# --- Pruebas del Caso de Uso ---

def test_user_creator_success():
    """
    Verifica que el caso de uso crea un usuario correctamente
    cuando el email no existe previamente.
    """
    # Arrange: Preparar el entorno de la prueba
    repository = FakeUserRepository()
    user_creator = UserCreator(user_repository=repository)
    command = CreateUserCommand(
        name="Test User",
        email="test@example.com",
        password="password123"
    )

    # Act: Ejecutar la lógica que se quiere probar
    user_creator.handle(command)

    # Assert: Verificar que el resultado es el esperado
    saved_user = repository.find_by_email("test@example.com")
    assert saved_user is not None
    assert saved_user.name == "Test User"
    assert saved_user.email == "test@example.com"
    assert saved_user.verify_password("password123")

def test_user_creator_fails_if_email_exists():
    """
    Verifica que el caso de uso lanza una excepción si el email
    del usuario ya existe en el repositorio.
    """
    # Arrange
    repository = FakeUserRepository()
    
    # Pre-cargar un usuario en el repositorio falso
    existing_user = User(
        name="Existing User",
        email="existing@example.com",
        hashed_password=User.hash_password("anypass")
    )
    repository.save(existing_user)
    
    user_creator = UserCreator(user_repository=repository)
    command = CreateUserCommand(
        name="Another User",
        email="existing@example.com", # Usar el mismo email
        password="password123"
    )

    # Act & Assert
    # with pytest.raises(ValueError, match="User with this email already exists."):
    #     user_creator.handle(command)
    with pytest.raises(ValueError, match="Usuario con este email ya existe"):
        user_creator.handle(command)
        