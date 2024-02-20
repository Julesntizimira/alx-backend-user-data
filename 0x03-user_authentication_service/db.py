#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar, Any


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        ''' create, save and return the user'''
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs: Any) -> TypeVar('User'):
        """
        takes in arbitrary keyword arguments and
        returns the first row found in the users
        table as filtered by the method's input arguments
        """
        for key, val in kwargs.items():
            try:
                user = self._session.query(User)\
                    .filter(getattr(User, key) == val).first()
            except Exception:
                from sqlalchemy.exc import InvalidRequestError
                raise InvalidRequestError
            if not user:
                from sqlalchemy.orm.exc import NoResultFound
                raise NoResultFound
            else:
                return user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        '''update user'''
        User_attr = User.__dict__.keys()
        User_attr = [attr for attr in User_attr if not attr.startswith('_')]
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in User_attr:
                raise ValueError
            setattr(user, key, val)
        self.__session.commit()
