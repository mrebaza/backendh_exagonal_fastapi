import pytest
from src.contexts.users.domain.entities import User

def test_user_creation():
    user = User(name="John Doe", email="john@test.com", hashed_password="somehash")
    assert user.name == "John Doe"
    assert "@" in user.email

def test_password_hashing_and_verification():
    password = "mysecretpassword"
    hashed_password = User.hash_password(password)
    
    user = User(name="Jane Doe", email="jane@test.com", hashed_password=hashed_password)
    
    assert user.hashed_password != password
    assert user.verify_password(password) is True
    assert user.verify_password("wrongpassword") is False