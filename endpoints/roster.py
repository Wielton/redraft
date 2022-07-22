from app import app
from flask import jsonify, request
from helpers.db_helpers import *
import uuid

@app.get('/api/rosters')
def get_rosters():
    params = request.args
    session_token = params.get('sessionToken')
    # Check session is valid 
    session_data = run_query("SELECT * FROM manager_session WHERE token=?", [session_token])
    print(session_data)
    # Grab manager_id
    manager_id = session_data[0][1]
    league_data = run_query("SELECT * FROM league_session WHERE manager_id=?",[manager_id])
    league_id = league_data[0][1]
    print(league_id)
    # Get the league_id to get the roster from that league
    roster_data = run_query("SELECT rosters.player_id,players.player, players.pos, players.team, team_logos.logo_url FROM rosters JOIN players ON players.id=rosters.player_id RIGHT JOIN team_logos ON team_logos.team_name=players.team WHERE rosters.league_id=? and rosters.manager_id=?",[league_id, manager_id])
    print(roster_data)
    resp = []
    for item in roster_data:
        roster = {}
        roster['playerId'] = item[0]
        roster['name'] = item[1]
        roster['position'] = item[2]
        roster['team'] = item[3]
        roster['logoUrl'] = item[4]
        resp.append(roster)
    return jsonify(resp), 200

@app.post('/api/rosters')
def add_to_roster(): 
    params = request.args
    session_token = params.get('sessionToken')
    player_id = params.get('playerId')
    manager_data = run_query("SELECT * FROM manager_session WHERE token=?", [session_token])
    # if manager_data is not None:
    manager_id = manager_data[0][1]
    leagues = run_query("SELECT * FROM league_session WHERE manager_id=?",[manager_id])
    league_id = leagues[0][1]
    run_query("INSERT INTO rosters (league_id, manager_id, player_id) VALUES (?,?,?)", [league_id, manager_id, player_id])
    return jsonify('Player added'), 200
        
                
    

