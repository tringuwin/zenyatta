




from automation.casting.utils.get_matchups_for_week import get_matchups_for_week
from context.context_helpers import get_league_season_constant_name
from helpers import get_constant_value
from safe_send import safe_send


async def update_score(db, message, team_name, score_change, context):

    team_name_lower = team_name.lower()

    league_season_constant = get_league_season_constant_name(context)
    league_season = get_constant_value(db, league_season_constant)

    
    schedule_plan = db['schedule_plans']
    season_schedule_plan = schedule_plan.find_one({'season': league_season, 'context': context})
    season_week = season_schedule_plan['current_week'] + 1
    
    matchups = get_matchups_for_week(db, context, league_season, season_week)

    found_matchup = None
    team_index = 0

    for matchup in matchups:
        if matchup['team1'].lower() == team_name_lower:
            found_matchup = matchup
            team_index = 1
            break
        elif matchup['team2'].lower() == team_name_lower:
            found_matchup = matchup
            team_index = 2
            break

    if not found_matchup:
        await safe_send(message.channel, 'Could not find a match this week that includes a team named '+team_name)
        return
    
    new_score_value = found_matchup['team'+str(team_index)+'_score'] + score_change

    map_win_array = found_matchup.get('map_win_array', [])
    if score_change > 0:
        map_win_array.append(found_matchup['team'+str(team_index)])
    else:
        if map_win_array and map_win_array[-1] == found_matchup['team'+str(team_index)]:
            map_win_array.pop()

    matchups_db = db['matchups']
    matchups_db.update_one({'matchup_id': found_matchup['matchup_id']}, {'$set': {'team'+str(team_index)+'_score': new_score_value, 'map_win_array': map_win_array}})

    await safe_send(message.channel, 'Score updated.')




async def add_point(db, message, context):

    command_parts = message.content.split()
    if len(command_parts) != 2:
        await safe_send(message.channel, 'Please send the name of the team to add a point to. Example: **!addpoint Polar**')
        return
    
    team_name = command_parts[1]

    await update_score(db, message, team_name, 1, context)


async def remove_point(db, message, context):

    command_parts = message.content.split()
    if len(command_parts) != 2:
        await safe_send(message.channel, 'Please send the name of the team to add a point to. Example: **!removepoint Polar**')
        return
    
    team_name = command_parts[1]

    await update_score(db, message, team_name, -1, context)


   
            
