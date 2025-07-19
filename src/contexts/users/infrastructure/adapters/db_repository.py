from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from ..persistence.user_model import UserModel
from ...domain.entities import User
from ...domain.repository import UserRepository

class DBUserRepository(UserRepository):
    """Adaptador que implementa el puerto UserRepository usando SQLAlchemy."""
    def __init__(self, db_session_factory: Session):
        self._session_factory = db_session_factory 

    def find_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        with self._session_factory() as session:
            user_model = session.query(UserModel).filter(UserModel.id == user_id).first()
            if user_model:
                return User(
                    id=user_model.id,
                    name=user_model.name,
                    email=user_model.email,
                    hashed_password=user_model.hashed_password
                )
        return None

    def save(self, user: User) -> None:
        with self._session_factory() as session:
            user_model = UserModel(
                id=user.id,
                name=user.name,
                email=user.email,
                hashed_password=user.hashed_password
            )
            session.add(user_model)
            session.commit()
        
    def find_by_email(self, email: str) -> Optional[User]:
        with self._session_factory() as session:
            user_model = session.query(UserModel).filter(UserModel.email == email).first()
            if user_model:
                return User(
                    id=user_model.id,
                    name=user_model.name,
                    email=user_model.email,
                    hashed_password=user_model.hashed_password
                )
        return None
    
    def find_all(self) -> List[User]:
        with self._session_factory() as session:
            user_models = session.query(UserModel).all()
            return [
                User(
                    id=user_model.id,
                    name=user_model.name,
                    email=user_model.email,
                    hashed_password=user_model.hashed_password
                )
                for user_model in user_models
            ]
        return None    