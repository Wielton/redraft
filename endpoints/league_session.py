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

@app.get('/api/league-session')
def enter_league():
    params = request.args
    # Check for valid session token
    session_token = params.get('sessionToken')
    league_id = params.get('leagueId')
    if session_token is None:   # If no session found then return error
        return jsonify("No session found"), 500
    manager_info = run_query("SELECT * FROM manager_session WHERE token=?",[session_token])
    # If valid token then retrieve client info 
    manager_id = manager_info[0][1]
    if manager_info is None:
        return jsonify("You must be logged in")
    else:
        print(manager_info)
            # Collect client info in resp list and return to client
        
        league_list = run_query("SELECT * FROM league_session WHERE manager_id=? AND league_id=?", [manager_id, league_id])
        print(league_list)
        resp = []
        for item in league_list:
            league = {}
            league['leagueId'] = item[0]
            league['name'] = item[2]
            resp.append(league)
        return jsonify(resp), 200
    
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