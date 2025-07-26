

from common_messages import invalid_number_of_params
from context.context_helpers import get_league_season_constant_name, get_league_teams_collection_from_context
from helpers import get_constant_value, valid_number_of_params


async def ff_match_handler(db, message, context):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    ff_team = params[1]

    league_teams_collection = get_league_teams_collection_from_context(db, context)
    ff_team_data = league_teams_collection.find_one({'name_lower': ff_team.lower()})

    if not ff_team_data:
        await message.channel.send(f'Team {ff_team} not found in the league context {context}.')
        return
    
    ff_team_name = ff_team_data['team_name']

    current_season_var = get_league_season_constant_name(context)
    current_season = get_constant_value(db, current_season_var)

    standings = db['standings']
    season_standings = standings.find_one({'context': context, 'season': current_season})

    if not season_standings:
        await message.channel.send(f'No standings found for the context {context} and season {current_season}.')
        return
    
    standings_forfeits = season_standings['forfeits']
    if ff_team_name in standings_forfeits:
        standings_forfeits[ff_team_name] += 1
    else:
        standings_forfeits[ff_team_name] = 1

    standings_teams = season_standings['teams']
    ff_team = standings_teams[ff_team_name]

    if 'forfeits' in ff_team:
        ff_team['forfeits'] += 1
    else:
        ff_team['forfeits'] = 1

    standings_teams[ff_team_name] = ff_team

    standings.update_one(
        {'context': context, 'season': current_season},
        {
            '$set': {
                'teams': standings_teams,
                'forfeits': standings_forfeits
            }
        }
    )

    await message.channel.send(f'{ff_team_name} has forfeited a match. Forfeits: {standings_forfeits[ff_team_name]}')


    
