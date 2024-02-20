#!/usr/bin/env python3
"""
 End-to-end integration test
"""
from uuid import uuid4
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> str:
    '''assert Auth.register_user'''
    form_data = {'email': email, 'password': password}
    response = requests.post('http://0.0.0.0:5200/users', data=form_data)
    resp = response.json()
    if response.status_code == 200:
        assert resp == {"email": email, "message": "user created"}
    elif response.status_code == 400:
        assert resp == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    '''login using a wrong password'''
    form_data = {'email': email, 'password': password}
    response = requests.post('http://0.0.0.0:5200/sessions', data=form_data)
    assert response.status_code == 401


def profile_unlogged() -> None:
    '''profile unlogged'''
    session_id = str(uuid4())
    cookies = {'session_id': session_id}
    response = requests.get('http://0.0.0.0:5200/profile', cookies=cookies)
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    '''log_in and return session_id'''
    form_data = {'email': email, 'password': password}
    response = requests.post('http://0.0.0.0:5200/sessions', data=form_data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_logged(session_id: str):
    '''profile unlogged'''
    cookies = {'session_id': session_id}
    response = requests.get('http://0.0.0.0:5200/profile', cookies=cookies)
    assert response.status_code == 200
    assert 'email' in response.json()


def log_out(session_id: str) -> None:
    '''logout session'''
    cookies = {'session_id': session_id}
    response = requests.delete('http://0.0.0.0:5200/sessions',
                               cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    '''get reset password token'''
    form_data = {'email': email}
    response = requests.post('http://0.0.0.0:5200/reset_password',
                             data=form_data)
    assert response.status_code == 200
    assert 'email' in response.json()
    assert 'reset_token' in response.json()
    return response.json().get('reset_token')


def update_password(email, reset_token, new_password) -> None:
    '''reset pasword'''
    form_data = {'email': email,
                 'reset_token': reset_token,
                 'new_password': new_password
                 }
    response = requests.put('http://0.0.0.0:5200/reset_password',
                            data=form_data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
