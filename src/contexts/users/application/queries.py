from pydantic import BaseModel
import uuid

class UserDTO(BaseModel):
    """DTO para transferir datos de usuario hacia el exterior."""
    id: uuid.UUID
    name: str
    email: str

    class Config:
        from_attributes = True # Anteriormente orm_mode