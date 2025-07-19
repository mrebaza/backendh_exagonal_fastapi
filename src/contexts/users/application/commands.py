from pydantic import BaseModel, Field, EmailStr
import uuid

class CreateUserCommand(BaseModel):
    """DTO para el comando de crear usuario."""
    # id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    email: EmailStr
    password: str