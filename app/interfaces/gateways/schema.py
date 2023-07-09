from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.interfaces.gateways.db import Base
from app.lib.security import encrypt_password_to_sha256


class User(Base):  # type: ignore
    """
    User
    """

    __tablename__ = "users"
    id = Column("id", Integer(), primary_key=True, autoincrement=True)
    name = Column("name", String(256), nullable=False, unique=True, index=True)
    password = Column("password", String(256), nullable=False)
    email = Column("email", String(256), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def __init__(
        self,
        name: str,
        password: str,
        email: str,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.name = name
        self.password = encrypt_password_to_sha256(password)
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
