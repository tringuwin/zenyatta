
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_role_by_id
from helpers import make_string_from_word_list
from league import remove_league_invite, update_team_info
from user import get_league_invites, get_league_team, user_exists

async def league_deny_handler(db, message):

    word_list = message.content.split()
    if len(word_list) < 2:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    team_name_to_deny = make_string_from_word_list(word_list, 1)
    team_name_lower = team_name_to_deny.lower()
    user_invites = get_league_invites(user)

    found_team = False
    for invite in user_invites:
        if invite.lower() == team_name_lower:
            found_team = True
            break

    if not found_team:
        await message.channel.send('You do not have a team invite from the team "'+team_name_to_deny+'". Please check the spelling of the team name.')
        return
    
    league_teams = db['leagueteams']
    league_team = league_teams.find_one({'name_lower': team_name_lower})
    real_team_name = league_team['team_name']
    
    remove_league_invite(user, real_team_name, db)

    await message.channel.send('Successfully removed the invite from that team.')
