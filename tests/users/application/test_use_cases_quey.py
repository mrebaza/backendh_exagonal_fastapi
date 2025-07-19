import pytest
import uuid
from typing import Dict, Optional
from unittest.mock import Mock
from src.contexts.users.application.use_cases_querys import UserFinder
from src.contexts.users.domain.entities import User
from src.contexts.users.domain.repository import UserRepository
from src.contexts.users.application.queries import UserDTO

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

def test_user_finder_finds_user_successfully():
    """
    Verifica que el caso de uso encuentra un usuario correctamente
    cuando existe en el repositorio.
    """
    # Arrange: Preparar el entorno de la prueba
    repository = FakeUserRepository()
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        name="Test User",
        email="test@example.com",
        hashed_password=User.hash_password("password123")
    )
    repository.save(user)
    
    user_finder = UserFinder(user_repository=repository)

    # Act: Ejecutar la lógica que se quiere probar
    result = user_finder.handle(user_id)

    # Assert: Verificar que el resultado es el esperado
    assert result is not None
    assert isinstance(result, UserDTO)
    assert result.id == user_id
    assert result.name == "Test User"
    assert result.email == "test@example.com"

def test_user_finder_returns_none_for_nonexistent_user():
    """
    Verifica que el caso de uso retorna None cuando el usuario
    no existe en el repositorio.
    """
    # Arrange
    repository = FakeUserRepository()
    user_finder = UserFinder(user_repository=repository)
    non_existent_user_id = uuid.uuid4()

    # Act
    result = user_finder.handle(non_existent_user_id)

    # Assert
    assert result is None

def test_user_finder_uses_repository_find_by_id():
    """
    Verifica que el caso de uso utiliza el método find_by_id
    del repositorio correctamente.
    """
    # Arrange
    # mock_repository = Mock(spec=UserRepository)
    # user_id = uuid.uuid4()
    # user_finder = UserFinder(user_repository=mock_repository)
    
    user_id = uuid.uuid4()
    mock_repository = Mock(spec=UserRepository)
    mock_user = User(id=user_id, name="Test User", email="test@example.com",hashed_password="hashedpassword123")  # objeto real
    # mock_user.hash_password("hashed")

    mock_repository.find_by_id.return_value = mock_user

    user_finder = UserFinder(user_repository=mock_repository)    

    # Act
    user_finder.handle(user_id)

    # Assert
    mock_repository.find_by_id.assert_called_once_with(user_id)