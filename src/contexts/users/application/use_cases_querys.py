from uuid import UUID
from ..domain.repository import UserRepository
from .queries import UserDTO

class UserFinder:
    """Caso de uso para encontrar un usuario por su ID."""
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository

    def handle(self, user_id: UUID) -> UserDTO | None:
        user = self._repository.find_by_id(user_id)
        if user:
            return UserDTO(id=user.id, name=user.name, email=user.email)
        return None