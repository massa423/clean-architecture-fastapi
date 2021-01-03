from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional
from datetime import datetime

from app.interfaces.gateways import db
from app.interfaces.gateways.schema import User
from app.exceptions.exception import DuplicateError, NoContentError
from app.core.logger import logger
from app.lib.security import encrypt_password_to_sha256

from sqlalchemy.exc import SQLAlchemyError, IntegrityError


class UserRepository(metaclass=ABCMeta):
    """
    UserRepository
    """

    @abstractmethod
    def find_users(self) -> Optional[List[Dict]]:
        """
        find_users
        """
        pass

    @abstractmethod
    def find_user_by_id(self, id: int) -> Optional[Dict]:
        """
        find_user_by_id
        """
        pass

    @abstractmethod
    def create_user(self, name: str, password: str, email: str) -> Optional[Dict]:
        """
        create_user
        """
        pass

    @abstractmethod
    def delete_user(self, id: int) -> Optional[Dict]:
        """
        delete_user
        """
        pass

    @abstractmethod
    def update_user(self, data_to_be_updated: Dict) -> Optional[Dict]:
        """
        update_user
        """
        pass


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
        except SQLAlchemyError:
            raise
        finally:
            db.session.close()
            logger.info("db connection closed.")

        if not user:
            raise NoContentError(("Users are not found."))

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
        except SQLAlchemyError:
            raise
        finally:
            db.session.close()

        if user is None:
            raise NoContentError(f"User not found: id={id}")

        return self.__convert_schema_obj_to_dict(user)

    def find_user_by_name(self, name: str) -> Optional[Dict]:
        """
        find_user_by_name
        """

        try:
            user = db.session.query(User).filter(User.name == name).first()
        except SQLAlchemyError:
            raise
        finally:
            db.session.close()

        if user is None:
            raise NoContentError(f"User not found: name={name}")

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
        except IntegrityError:
            db.session.rollback()

            raise DuplicateError(f"name: {name} or email: {email} is already exists.")
        except SQLAlchemyError:
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
        except SQLAlchemyError:
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
        except SQLAlchemyError:
            raise
        finally:
            db.session.close()

        if deleted_user is None:
            raise NoContentError

        try:
            db.session.query(User).filter(User.id == id).delete()
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
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

        # パスワード暗号化
        if data_to_be_updated.get("password") is not None:
            data_to_be_updated["password"] = encrypt_password_to_sha256(
                data_to_be_updated["password"]
            )

        try:
            db.session.query(User).filter(User.id == data_to_be_updated["id"]).update(
                data_to_be_updated
            )
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise DuplicateError(e)
        except SQLAlchemyError:
            raise
        finally:
            db.session.close()

        try:
            updated_user = (
                db.session.query(User)
                .filter(User.id == data_to_be_updated["id"])
                .first()
            )
        except SQLAlchemyError:
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
