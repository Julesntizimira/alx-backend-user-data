#!/usr/bin/env python3
'''
User model
'''
from sqlalchemy import Column, String, INTEGER 
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    '''represent User model
    '''
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
