

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params


async def init_standings(db, message):
    
    standings_db = db['standings']
    num_seasons = standings_db.count_documents({})

    new_season_num = num_seasons + 1

    all_teams = {}

    leagueteams = db['leagueteams']
    all_db_teams = leagueteams.find()
    for team in all_db_teams:
        new_team_obj = {
            'wins': 0,
            'losses': 0,
            'map_wins': 0,
            'map_losses': 0,
            'points': 0
        }
        all_teams[team['team_name']] = new_team_obj

    season_obj = {
        'season': new_season_num,
        'teams': all_teams
    }

    standings_db.insert_one(season_obj)

    await message.channel.send('Standings created for Season '+str(new_season_num))