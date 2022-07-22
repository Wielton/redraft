# This is the manager endpoint for signing up, getting and
#  patching info, and deleting account

from app import app
from flask import jsonify, request
from helpers.db_helpers import *
import bcrypt
import uuid


# Bcrypt password encryption handling

def encrypt_password(password):
    salt = bcrypt.gensalt(rounds=5)
    hash_result = bcrypt.hashpw(password.encode(), salt)
    print(hash_result)
    decrypted_password = hash_result.decode()
    return decrypted_password

# Response Codes: 
#   1. 200 = Success manager creation
#   2. 204 = success with No Content, which would be if nothing was edited in the user profile

# Error Codes: 
#   1. 401 = Access Denied because of lack of valid session token
#   2. 422 = Unprocessable because of lacking required info from manager 
#   3. 500 = Internal Server Error



@app.post('/api/manager')
def manager_register():
    data = request.json
    email = data.get('email')
    username = data.get('username')
    password_input = data.get('password')
    password = encrypt_password(password_input)
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    
    if not email:
        return jsonify("Email required"), 422
    if not username:
        return jsonify("Username required"), 422
    if not password_input:
        return jsonify("Password required"), 422
    if not first_name:
        return jsonify("First Name required"), 422
    if not last_name:
        return jsonify("Last name required"), 422

    run_query("INSERT INTO manager (email, username, password, first_name, last_name) VALUES (?,?,?,?,?)", [email, username, password, first_name, last_name])
    
    # Use cursor.lastrow() instead of using a SELECT query
    manager_data = run_query("SELECT * FROM manager WHERE username=?", [username])
    
    token = str(uuid.uuid4().hex)
    
    manager_id = manager_data[0][0]
    run_query("INSERT INTO manager_session (manager_id,token) VALUES (?,?)", [manager_id,token])
    
    return jsonify("Registered"),201  
# Manager redirected to logged-in where they see  


@app.patch('/api/manager')
def edit_profile():
    # GET params for session check
    params = request.args
    session_token = params.get('token')
    if not session_token:
        return jsonify("Session token not found!"), 401
    manager_info = run_query("SELECT * FROM manager JOIN manager_session ON manager_session.manager_id=manager.id WHERE token=?",[session_token])
    if manager_info is not None:
        manager_id = manager_info[0][0]
        data = request.json
        build_statement = ""
        # string join
        build_vals = []
        if data.get('username'):
            new_username = data.get('username')
            build_vals.append(new_username)
            build_statement+="username=?"
        else:
            pass
        if data.get('password'):
            new_password_input = data.get('password')
            new_password = encrypt_password(new_password_input)
            build_vals.append(new_password)
            if ("username" in build_statement):
                build_statement+=",password=?"
            else:
                build_statement+="password=?"
        else:
            pass
        if data.get('firstName'):
            new_first_name = data.get('firstName')
            build_vals.append(new_first_name)
            if ("username" in build_statement) or ("password" in build_statement):
                build_statement+=",first_name=?"
            else:
                build_statement+="first_name=?"
        else:
            pass
        if data.get('lastName'):
            new_last_name = data.get('lastName')
            build_vals.append(new_last_name)
            if ("username" in build_statement) or ("password" in build_statement) or ("first_name" in build_statement):
                build_statement+=",last_name=?"
            else:
                build_statement+="last_name=?"
        else:
            pass
        build_vals.append(manager_id)
        statement = str(build_statement)
        run_query("UPDATE manager SET "+statement+" WHERE id=?", build_vals)
        # Create error(500) for the server time out, or another server issue during the update process
        return jsonify("Your info was successfully edited"), 204
    else:
        return jsonify("Session not found"), 500

@app.delete('/api/manager')
def delete_account():
    params = request.args
    session_token = params.get('token')
    if not session_token:
        return jsonify("Session token not found!"), 401
    session = run_query("SELECT * FROM manager_session WHERE token=?",[session_token])
    if session is not None:
        user_id = session[0][3]
        run_query("DELETE FROM manager_session WHERE token=?",[session_token])
        run_query("DELETE FROM manager WHERE id=?",[user_id])
        return jsonify("Account deleted"), 204
    else:
        return jsonify("You must be logged in to delete your account"), 500