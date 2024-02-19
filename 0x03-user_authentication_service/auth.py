#!/usr/bin/env python3
"""
auth module
"""
import bcrypt
from db import DB
from typing import TypeVar


def _hash_password(password: str) -> bytes:
    '''hash password'''
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        '''register user'''
        try:
            self._db.find_user_by(email=email)
        except Exception:
            hashed_password = _hash_password(password)
            return self._db.add_user(email=email,
                                     hashed_password=hashed_password)
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        '''Credentials validation'''
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        '''return a string representation of a new UUID'''
        import uuid
        id = str(uuid.uuid4())
        return id

    def create_session(self, email: str) -> str:
        '''Get session ID'''
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        myid = self._generate_uuid()
        self._db.update_user(user.id, session_id=myid)
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        '''returns the corresponding User or None'''
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        The method updates the corresponding
        users session ID to None
        """
        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        generate a UUID and update the user's
        reset_token database field
        """
        try:
            user = self._db.find_user_by(email=email)
            token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''Update Password'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password=password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
        except Exception:
            raise ValueError
