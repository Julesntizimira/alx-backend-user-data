#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    '''manage the API authentication
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''Define which routes don't need authentication'''
        if not path:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path = path + '/'
        for endpoint in excluded_paths:
            if endpoint[-1] == "*":
                endpoint = endpoint[:-1]
                if endpoint in path:
                    return False
            elif endpoint == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        '''Request validation'''
        if not request:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''return None'''
        return None

    def session_cookie(self, request=None) -> str:
        '''returns a cookie value from a request'''
        if not request:
            return None
        import os
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
