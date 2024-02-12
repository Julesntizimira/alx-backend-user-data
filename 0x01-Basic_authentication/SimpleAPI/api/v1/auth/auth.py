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
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        '''return None'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''return None'''
        return None
