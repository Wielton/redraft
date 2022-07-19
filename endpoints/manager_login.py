from app import app
from flask import jsonify, request
from helpers.db_helpers import *
import bcrypt
import uuid



# Client login/logout endpoint

@app.post('/api/manager-login')
def manager_login():
    data = request.json
    email_input = data.get('loginEmail')
    password_input = data.get('loginPassword')
    manager_info = run_query("SELECT * FROM manager WHERE email=?", [email_input])
    print(manager_info)
    manager_password = manager_info[0][3]
    manager_id = manager_info[0][0]
    if manager_info is not None:
        manager = {}
        if not bcrypt.checkpw(password_input.encode(), manager_password.encode()):
            return jsonify("Error"),401
        login_token = str(uuid.uuid4().hex)
        logged_in = run_query("SELECT * FROM manager_session WHERE manager_id=?",[manager_id])
        if logged_in is None:
            run_query("INSERT INTO manager_session (manager_id,token) VALUES (?,?)", [manager_id,login_token])
        elif manager_id == logged_in[0][1]:
            # I could UPDATE here but I chose to delete then create a new session instance as I figured this is a better thing to do because of token lifecycles and other errors that could occur from just updating one column
            run_query("DELETE FROM manager_session WHERE manager_id=?",[manager_id])
            run_query("INSERT INTO manager_session (manager_id, token) VALUES (?,?)", [manager_id,login_token])
        manager['managerId'] = manager_id
        manager['sessionToken'] = login_token
        print(manager)
        return jsonify(manager),201
    else:
        return jsonify("Email not found.  PLease try again"), 500


@app.delete('/api/manager-login')
def manager_logout():
    params = request.args
    session_token = params.get('sessionToken')
    session = run_query("SELECT * FROM manager_session WHERE token=?",[session_token])
    if session is None:
        return jsonify("You're not logged in."), 404
    else:
        run_query("DELETE FROM manager_session WHERE token=?",[session_token])
        return jsonify("Manager logged out"),204