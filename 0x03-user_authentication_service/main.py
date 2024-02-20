#!/usr/bin/env python3
"""
 End-to-end integration test
"""
import json
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email, password):
    '''assert Auth.register_user'''
    form_data = {'email': email, 'password': password}
    response = requests.post('http://0.0.0.0:5200/users', data=form_data)
    resp = response.json()
    if response.status_code == 200:
        assert json.loads(resp) == {"email": email, "message": "user created"}
    elif response.status_code == 400:
        assert json.loads(resp) == {"message": "email already registered"}




if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    '''log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)'''