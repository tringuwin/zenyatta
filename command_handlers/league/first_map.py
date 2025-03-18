



from common_messages import not_registered_response
from context.context_helpers import get_league_team_field_from_context
from user import user_exists


def find_user_matchup(db, league_team, context):

    matchups = db['matchups']

    my_matchup = matchups.find_one({'context': context, 'team1': league_team})
    if my_matchup:
        return my_matchup
    
    my_matchup = matchups.find_one({'context': context, 'team2': league_team})
    if my_matchup:
        return my_matchup
    
    return None

async def first_map_handler(db, message, context):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return

    league_team_field = get_league_team_field_from_context(context)
    if not (league_team_field in user):
        await message.channel.send('You are not on a league team.')
        return
    
    league_team = user[league_team_field]
    if league_team == 'None':
        await message.channel.send('You are not on a league team.')
        return
    
    user_matchup = find_user_matchup(db, league_team, context)
    if not user_matchup:
        await message.channel.send('You do not have a matchup scheduled for this week.')
        return
    
    team1 = user_matchup['team1']
    team2 = user_matchup['team2']
    await message.channel.send(f'The first map for your matchup ({team1} VS {team2}) this week is: '+user_matchup['first_map'])


