



from automation.casting.utils.get_matchups import get_matchups_for_week
from context.context_helpers import get_league_season_constant_name
from helpers import get_constant_value


async def swap_sides(db, message, context):

    command_parts = message.content.split()
    if len(command_parts) != 2:
        await message.channel.send('Please send the name of one of the two teams playing in the match to swap. Example: **!swapsides Polar**')
        return
    team_name = command_parts[1]
    team_name_lower = team_name.lower()

    league_season_constant = get_league_season_constant_name(context)
    league_season = get_constant_value(db, league_season_constant)

    schedule_plans = db['schedule_plans']
    season_schedule_plan = schedule_plans.find_one({'season': league_season, 'context': context})

    if not season_schedule_plan:
        await message.channel.send('Could not find a schedule for that current season.')
        return

    league_week = season_schedule_plan['current_week'] + 1

    matchups = get_matchups_for_week(db, context, league_season, league_week)


    found_matchup = False
    for matchup in matchups:
        if matchup['team1'].lower() == team_name_lower or matchup['team2'].lower() == team_name_lower:
            found_matchup = matchup
            break

    if not found_matchup:
        await message.channel.send('Could not find a match this week that includes a team named '+team_name)
        return
    
    
    new_left_team = 1 if matchup['left_team'] == 2 else 2

    matchups = db['matchups']
    matchups.update_one({'matchup_id': matchup['matchup_id']}, {'$set': {'left_team': new_left_team}})

    await message.channel.send('Swapped sides.')
            
