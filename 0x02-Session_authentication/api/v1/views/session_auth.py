#!/usr/bin/env python3
""" Module of session authantication
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
def session_authentication() -> str:
    '''session authantication'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        user_list = User.search({'email': email})
        if not user_list or len(user_list) == 0:
            return jsonify({"error": "no user found for this email"}), 404
        user = None
        for obj in user_list:
            if obj.is_valid_password(password):
                user = obj
        if not user:
            return jsonify({"error": "wrong password"}), 404
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        cookie_name = os.getenv('SESSION_NAME')
        resp = make_response(jsonify(user.to_json()))
        resp.set_cookie(cookie_name, session_id)
        return resp
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404


@app_views.route('/auth_session/logout/',
                 methods=['DELETE'], strict_slashes=False)
def session_logout() -> str:
    '''session logout'''
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
