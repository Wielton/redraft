from app import app
from flask import jsonify, request
from helpers.db_helpers import *
from helpers.scoring_functions import *

# Currently I'm taking a single playerId to get the points for that week
# but I need to take in the whole roster with the rosterID and managerId and leagueId
# as arguments  

@app.get('/api/scoring')
def get_scores():
    data = request.json
    player_id = data.get('playerId')
    player = run_query("SELECT * FROM players WHERE id=?",[player_id])
    player_name = player[0][1]
    player_position = player[0][2]
    players_scores = run_query("SELECT * FROM week1_stats WHERE player=?",[player_name])
    print(players_scores)
    resp = []
    for item in players_scores:
        player_stats = {}
        if player_position == "QB":
            player_stats['name'] = item[0]
            player_stats['comp'] = int(item[2])
            player_stats['att'] = int(item[3])
            player_stats['passYds'] = int(item[4])
            player_stats['passTds'] = int(item[5])
            player_stats['passInt'] = int(item[6])
            resp.append(player_stats)
        elif (player_position == "RB") or (player_position == "WR") or (player_position == "TE"):
            player_stats['name'] = item[0]
            player_stats['rushAtt'] = int(item[11])
            player_stats['rushYds'] = int(item[12])
            player_stats['rushTds'] = int(item[13])
            player_stats['recTgts'] = int(item[15])
            player_stats['rec'] = int(item[16])
            player_stats['recYds'] = int(item[17])
            player_stats['recTDs'] = int(item[18])
            player_stats['fmbLost'] = int(item[21])
            resp.append(player_stats)
            yd_pts(int(item[12]))
            td_pts(int(item[13]))
            yd_pts(int(item[17]))
            td_pts(int(item[18]))
            # print(,td_pts(int(item[13])),yd_pts(int(item[17])),td_pts(int(item[18])))
    # print(name + " scored " + total + " points this week")
    return jsonify(resp), 200

# @app.post('/api/rosters')
# def add_player():
#     players_list = run_query("SELECT * FROM players")
#     print(players_list)
#     resp = []
#     for item in players_list:
#         restaurant = {}
#         restaurant['name'] = item[1]
#         restaurant['position'] = item[2]
#         restaurant['team'] = item[3]
#         restaurant['ADP'] = item[4]
#         restaurant['ovrRank'] = item[7]
#         restaurant['posRank'] = item[8]
#         resp.append(restaurant)
#     return jsonify(resp), 200