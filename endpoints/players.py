from app import app
from flask import jsonify, request
from helpers.db_helpers import *

# Restaurant get, signup and edit




@app.get('/api/players')
def get_players():
    #  Take in the sessionToken to check session and then retrieve managerId
    params = request.args
    session_token = params.get('sessionToken')
    manager_data = run_query("SELECT * FROM manager_session WHERE token=?",[session_token])
    manager_id = manager_data[0][1]
    #  Use managerId to retrieve and store leagueId
    league_data = run_query("SELECT * FROM league_session WHERE manager_id=?",[manager_id])
    league_id = league_data[0][1]
    #  Use leagueId to retrieve and store roster data
    roster_ids = run_query("SELECT player_id FROM rosters WHERE league_id=?",[league_id])
    # I need to SELECT and JOIN players who are linked to the league
    players_list = run_query("SELECT players.id, players.player,players.pos,players.team,players.current_adp,team_logos.logo_url FROM players INNER JOIN team_logos ON team_logos.team_name=players.team")
    unavailable_players = []
    for index, roster_player in enumerate(roster_ids):
        unavailable_players.append(roster_player[0])
    # Unavailable_players is now a list of player_ids as INT
    # print("These are unavailable player_ids: ",index, ":", unavailable_players)
    
    master_players_list = []
    # available_players = []
    for index, master_players in enumerate(players_list):
        master_players_list.append(master_players[0])
    #     if roster_player[0] != players_list[0]:
    #         available_players.append(master_players)
    # # Master player list player ids as INT
    # print("These are master player_ids: ",index, ":", master_players_list)
    
    #  I have a master player list and an unavailable player list
    
    sorted_unavailable_players = sorted(unavailable_players)
    print(master_players_list)
    print(sorted_unavailable_players)
    final_players = []
    for i in master_players_list[:]:
        if i not in sorted_unavailable_players:
            final_players.append(i)
    resp = []
    for players in final_players:
        player = {}
        player['playerId'] = players
        # player['name'] = players[1]
        # player['position'] = players[2]
        # player['team'] = players[3]
        # player['adp'] = players[4]
        # player['logoUrl'] = players[5]
        resp.append(player)
    return jsonify(resp), 200





