#!/usr/bin/env python3
""" UserSession module
"""
from models.base import Base


class UserSession(Base):
    '''UserSession Model that inherits from base
    '''
    def __init__(self, *args: list, **kwargs: dict):
        '''constructor method'''
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
