#!/usr/bin/env python3
""" Session exipiration
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''manage session expiration'''
    def __init__(self):
        '''constructor method
        '''
        dur = os.getenv('SESSION_DURATION')
        if not dur or not isinstance(int(dur), int):
            self.session_duration = 0
        else:
            self.session_duration = int(dur)

    def create_session(self, user_id=None):
        '''overrode super().create_session'''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''overrode super().user_id_for_session_id'''
        if not session_id or not self.user_id_by_session_id.get(session_id):
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get('user_id')
        created_at = self.user_id_by_session_id.get(session_id)\
            .get('created_at')
        if not created_at:
            return None
        if created_at + timedelta(seconds=self.session_duration
                                  ) <= datetime.now():
            return None
        return self.user_id_by_session_id.get(session_id).get('user_id')
