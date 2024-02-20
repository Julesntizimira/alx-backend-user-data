#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Union, Any, NoReturn, Dict
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


User_attr = User.__dict__.keys()
User_attr = [attr for attr in User_attr if not attr.startswith('_')]


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

    def add_user(self, email: str, hashed_password: str) -> User:
        ''' create, save and return the user'''
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        takes in arbitrary keyword arguments and
        returns the first row found in the users
        table as filtered by the method's input arguments
        """
        for key, val in kwargs.items():
            if key not in User_attr:
                raise InvalidRequestError
            user = self._session.query(User)\
                .filter(getattr(User, key) == val).first()
            break
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        '''update user'''
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if key not in User_attr:
                raise ValueError
            setattr(user, key, val)
        self.__session.commit()
