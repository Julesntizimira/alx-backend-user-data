#!/usr/bin/env python3
"""
BasicAuth class
"""
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    '''BasicAuth class'''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''basic Base64'''
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        '''Base64 decode'''
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            import base64
            b64 = base64_authorization_header.encode("utf8")
            encoded_utf8 = base64.b64decode(b64)
            decoded_utf_str = encoded_utf8.decode("utf-8")
        except Exception:
            return None
        return decoded_utf_str

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        '''User credentials'''
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(":"))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''User instance based on his
           email and password
        '''
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        from models.user import User
        user_list = User.search({"email": user_email})
        if len(user_list) == 0:
            return None
        if user_list[0].is_valid_password(user_pwd) is True:
            return user_list[0]
        return None
