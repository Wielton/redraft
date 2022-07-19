from flask import Flask

# Only a single app object is allowed
app = Flask(__name__)

from endpoints import players, scoring, manager, manager_login, league, roster, all_manager_rosters, league_session