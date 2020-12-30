from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime

from app.interfaces.gateways import db
from app.interfaces.gateways.schema import User
from app.exceptions.exception import DuplicateError, NoContentError

from sqlalchemy.exc import IntegrityError


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

    @abstractmethod
    def create_user(self, name: str, password: str, email: str) -> Optional[Dict]:
        """
        create_user
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
        user: User = None

        try:
            user = db.session.query(User).all()
        except Exception as e:
            print(e)
            raise
        finally:
            db.session.close()

        if not user:
            print("Users are not found.")
            raise NoContentError

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

        try:
            user = db.session.query(User).filter(User.id == id).first()
        except Exception as e:
            print(e)
            raise
        finally:
            db.session.close()

        if user is None:
            print(f"id={id} is not found.")
            raise NoContentError

        response = {
            "id": user.id,
            "name": user.name,
            "password": user.password,
            "email": user.email,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        return response

    def create_user(self, name: str, password: str, email: str) -> Optional[Dict]:
        """
        create_user
        """

        now = datetime.now()
        created_user = None

        user = User(
            name=name,
            password=password,
            email=email,
            created_at=now,
            updated_at=now,
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(e)

            raise DuplicateError
        except Exception as e:
            print(e)
            raise
        finally:
            db.session.close()

        try:
            created_user = (
                db.session.query(User)
                .filter(User.name == name)
                .order_by(User.id.desc())
                .first()
            )
        except Exception as e:
            print(e)
            raise NoContentError
        finally:
            db.session.close()

        response = {
            "id": created_user.id,
            "name": created_user.name,
            "password": created_user.password,
            "email": created_user.email,
            "created_at": created_user.created_at,
            "updated_at": created_user.updated_at,
        }
        return response
