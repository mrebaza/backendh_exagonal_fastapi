import uuid
import re
from dataclasses import dataclass, field
from passlib.context import CryptContext

# Usamos passlib para un manejo seguro de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@dataclass
class User:
    """
    Esta es la entidad principal o Agregado del contexto.
    No tiene dependencias de frameworks. Es puro Python.
    """
    name: str
    email: str
    hashed_password: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if not self.name:
            raise ValueError("El nombre no puede estar vacío")
        if not self._is_valid_email(self.email):
            raise ValueError("El email no es válido")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @classmethod
    def create(cls, name: str, email: str) -> 'User':
        return cls(id=uuid.uuid4(), name=name, email=email)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
