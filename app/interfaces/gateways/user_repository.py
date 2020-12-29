from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional

from app.interfaces.gateways import db
from app.interfaces.gateways.schema import User


class UserRepository(metaclass=ABCMeta):
    """
    UserRepository
    """

    @abstractmethod
    def find_users(self) -> Optional[List[Dict]]:
        """
        find_users
        """
        raise NotImplementedError

    @abstractmethod
    def find_user_by_id(self, id: int) -> Optional[Dict]:
        """
        find_user_by_id
        """
        raise NotImplementedError


class UserRepositoryImpl(UserRepository):
    """
    UserRepositoryImpl
    """

    def find_users(self) -> Optional[List[Dict]]:
        """
        find_users
        """
        user = db.session.query(User).all()
        db.session.close()

        if user is None:
            return None

        response = []
        for u in user:
            response.append(
                {
                    "id": u.id,
                    "name": u.name,
                    "password": u.password,
                    "email": u.email,
                    "created_at": u.created_at,
                    "updated_at": u.updated_at,
                }
            )
        return response

    def find_user_by_id(self, id: int) -> Optional[Dict]:
        """
        find_user_by_id
        """

        user = db.session.query(User).filter(User.id == id).first()
        db.session.close()

        if user is None:
            return None

        response = {
            "id": user.id,
            "name": user.name,
            "password": user.password,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        return response
