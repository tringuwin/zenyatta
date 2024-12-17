
from common_messages import invalid_number_of_params
from helpers import make_string_from_word_list
from league_helpers import get_league_team_with_context, get_league_teams_collection
from user import get_league_team, user_exists


async def change_team_owner_handler(db, message, context):

    word_parts = message.content.split()
    if len(word_parts) < 3:
        await invalid_number_of_params(message)
        return
    
    league_teams = get_league_teams_collection(db, context)
    team_name = make_string_from_word_list(word_parts, 2)
    team_obj = league_teams.find_one({'team_name': team_name})
    if not team_obj:
        await message.channel.send('Could not find team "'+team_name+'"')
        return
    
    mentions = message.mentions
    if len(mentions) != 1:
        await message.channel.send('Please mention 1 user to make the team owner')
        return
    
    mention_member = mentions[0]
    user = user_exists(db, mention_member.id)
    if not user:
        await message.channel.send('That user is not registered')
        return
    
    user_league_team = get_league_team_with_context(user, context)
    if user_league_team != team_name:
        await message.channel.send('That user is not part of this team.')
        return
    
    old_owner_id = team_obj['owner_id']

    for member in team_obj['members']:
        if member['discord_id'] == old_owner_id:
            member['is_owner'] = False
            member['is_admin'] = False
        elif member['discord_id'] == mention_member.id:
            member['is_owner'] = True
            member['is_admin'] = True

    league_teams.update_one({'team_name': team_name}, {"$set": {"members": team_obj['members'], 'owner_id': mention_member.id}})

    await message.channel.send('League Team owner changed')


