from abc import ABC, abstractmethod
from typing import Optional
import uuid
from .entities import User

class UserRepository(ABC):
    """
    Este es un Puerto. Define las operaciones que la capa de aplicación
    puede realizar sobre el repositorio de usuarios, sin saber cómo se implementa.
    """
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass