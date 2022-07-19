# This is the league endpoint for signing up, getting and
#  patching info, and deleting account

from app import app
from flask import jsonify, request
from helpers.db_helpers import *
import bcrypt
import uuid


# Bcrypt password encryption handling



# Response Codes: 
#   1. 200 = Success manager creation
#   2. 204 = success with No Content, which would be if nothing was edited in the user profile

# Error Codes: 
#   1. 401 = Access Denied because of lack of valid session token
#   2. 422 = Unprocessable because of lacking required info from manager 
#   3. 500 = Internal Server Error

# Get manager info

@app.get('/api/leagues')
def get_league_info():
    params = request.args
    # Check for valid session token
    session_token = params.get('sessionToken')
    if session_token is None:   # If no session found then return error
        return jsonify("No session found"), 500
    manager_info = run_query("SELECT * FROM manager_session WHERE token=?",[session_token])
    # If valid token then retrieve client info 
    if manager_info is None:
        return jsonify("You must be logged in")
    else:
        print(manager_info)
            # Collect client info in resp list and return to client
        manager_id = manager_info[0][1]
        league_list = run_query("SELECT * FROM leagues WHERE manager_id=?", [manager_id])
        print(league_list)
        resp = []
        for item in league_list:
            league = {}
            league['leagueId'] = item[0]
            league['name'] = item[2]
            resp.append(league)
        return jsonify(resp), 200
            


@app.post('/api/leagues')
def league_register():
    data = request.json
    params = request.args
    session_token = params.get('sessionToken')
    league_name = data.get('leagueName')
    # Check session is valid 
    session_data = run_query("SELECT * FROM manager_session WHERE token=?", [session_token])
    print(session_data)
    # Grab manager_id
    manager_id = session_data[0][1]
    invite_key = str(uuid.uuid4().hex)
    run_query("INSERT INTO leagues (manager_id, name, invite_key) VALUES (?,?,?)", [manager_id, league_name, invite_key])
    # Use cursor.lastrow() instead of using a SELECT query
    return jsonify('Manager account created successfully.', invite_key), 201
# Manager redirected to logged-in where they see  


@app.post('/api/league-session')
def join_league():
    data = request.json
    params = request.args
    session_token = params.get('sessionToken')
    invite_key = data.get('inviteKey')
    # Do I need to get this session token?
    manager_session = run_query("SELECT * FROM manager_session WHERE token=?", [session_token])
    if manager_session is not None:
        manager_id = manager_session[0][1]
        session = run_query('SELECT * FROM leagues WHERE invite_key=?',[invite_key])
        if session is not None:
            league_id = session[0][0]
            league_name = session[0][2]
            run_query("INSERT INTO league_session (league_id, manager_id, invite_key) VALUES (?,?,?)",[league_id, manager_id,invite_key])
        return jsonify('Manager joined the ', league_name, ' league!')