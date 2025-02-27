
from common_messages import invalid_number_of_params, not_registered_response
from context_helpers import get_league_teams_collection_from_context
from helpers import make_string_from_word_list
from league import remove_league_invite
from user import get_league_invites_with_context, user_exists

async def league_deny_handler(db, message, context):

    word_list = message.content.split()
    if len(word_list) < 2:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    team_name_to_deny = make_string_from_word_list(word_list, 1)
    team_name_lower = team_name_to_deny.lower()
    user_invites = get_league_invites_with_context(user, context)

    found_team = False
    for invite in user_invites:
        if invite.lower() == team_name_lower:
            found_team = True
            break

    if not found_team:
        await message.channel.send('You do not have a team invite from the team "'+team_name_to_deny+'". Please check the spelling of the team name.')
        return
    
    league_teams = get_league_teams_collection_from_context(db, context)
    league_team = league_teams.find_one({'name_lower': team_name_lower})
    real_team_name = league_team['team_name']
    
    remove_league_invite(user, real_team_name, db, context)

    await message.channel.send('Successfully removed the invite from that team.')
