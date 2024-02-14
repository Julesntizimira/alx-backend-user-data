#!/usr/bin/env python3
""" SessionDBAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    '''SessionDBAuth'''
    def create_session(self, user_id=None) -> str:
        '''creates and stores new instance of UserSession
           overload super().create_session
        '''
        if not user_id:
            return None
        session_id = str(uuid.uuid4())
        attr_dict = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**attr_dict)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        '''returns the User ID by requesting UserSession
           in the database based on session_id
        '''
        if not session_id or not isinstance(session_id, str):
            return None
        usersession_list = UserSession.search({'session_id': session_id})
        if not usersession_list or len(usersession_list) == 0:
            return None
        usersession = usersession_list[0]
        created_at = usersession.created_at
        if created_at + timedelta(seconds=self.session_duration
                                  ) <= datetime.utcnow():
            return None
        user_id = usersession.user_id
        return user_id

    def destroy_session(self, request=None) -> bool:
        '''destroys the UserSession based on
           the Session ID from the request cookie
        '''
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id or not self.user_id_for_session_id(session_id):
            return False
        usersession_list = UserSession.search({'session_id': session_id})
        usersession = usersession_list[0]
        usersession.remove()
        return True
