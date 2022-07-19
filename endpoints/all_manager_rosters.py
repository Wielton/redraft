from app import app
from flask import jsonify, request
from helpers.db_helpers import *
import uuid

@app.get('/api/all-manager-rosters')
def get_all_rosters():
    data = request.args
    manager_id = data.get('managerId')
    roster_data = run_query("SELECT rosters.manager_id, players.player, players.pos,players.team FROM rosters RIGHT JOIN players ON players.id=rosters.player_id WHERE rosters.manager_id=?",[manager_id])
    print(roster_data)
    resp = []
    for item in roster_data:
        roster = {}
        roster['managerId'] = item[0]
        roster['playerName'] = item[1]
        roster['playerPos'] = item[2]
        roster['playerTeam'] = item[3]
        resp.append(roster)
    return jsonify(resp), 200