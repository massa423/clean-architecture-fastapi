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

    @abstractmethod
    def delete_user(self, id: int) -> Optional[Dict]:
        """
        delete_user
        """
        raise NotImplementedError

    @abstractmethod
    def update_user(self, data_to_be_updated: Dict) -> Optional[Dict]:
        """
        update_user
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
            response.append(self.__convert_schema_obj_to_dict(u))

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

        return self.__convert_schema_obj_to_dict(user)

    def create_user(self, name: str, password: str, email: str) -> Optional[Dict]:
        """
        create_user
        """

        now = datetime.now()

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

        return self.__convert_schema_obj_to_dict(created_user)

    def delete_user(self, id: int) -> Optional[Dict]:
        """
        delete_user
        """
        try:
            deleted_user = db.session.query(User).filter(User.id == id).first()
        except Exception as e:
            print(e)
            raise
        finally:
            db.session.close()

        if deleted_user is None:
            raise NoContentError

        try:
            db.session.query(User).filter(User.id == id).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            raise
        finally:
            db.session.close()

        return self.__convert_schema_obj_to_dict(deleted_user)

    def update_user(self, data_to_be_updated: Dict) -> Optional[Dict]:
        """
        update_user
        """
        now = datetime.now()
        data_to_be_updated["updated_at"] = now

        try:
            db.session.query(User).filter(User.id == data_to_be_updated["id"]).update(
                data_to_be_updated
            )
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
            updated_user = (
                db.session.query(User)
                .filter(User.id == data_to_be_updated["id"])
                .first()
            )
        except Exception as e:
            print(e)
            raise NoContentError
        finally:
            db.session.close()

        return self.__convert_schema_obj_to_dict(updated_user)

    def __convert_schema_obj_to_dict(self, schema: User) -> Dict:
        """
        行オブジェクトを辞書型に変換する。
        """
        return {
            "id": schema.id,
            "name": schema.name,
            "password": schema.password,
            "email": schema.email,
            "created_at": schema.created_at,
            "updated_at": schema.updated_at,
        }
