#!/usr/bin/env python3
"""falsk app module
"""
from flask import Flask, jsonify, request, abort
from flask import make_response, redirect, url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    '''testing the app'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    '''register user'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    '''login'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or not password:
        abort(401)
    if AUTH.valid_login(email=email, password=password) is False:
        abort(401)
    myid = AUTH.create_session(email=email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", myid)
    return resp


@app.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    '''logout'''
    session_id = request.form.get('session_id')
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        AUTH.destroy_session(session_id)
        return redirect('/')
    abort(403)


@app.route('/profile', strict_slashes=False)
def get_profile():
    '''get user profile'''
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    '''get reset password'''
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email=email)
        return jsonify({"email": email, "reset_token": token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    '''Reset password'''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token=reset_token, password=new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
