
from api import give_role
from discord_actions import get_role_by_id
from helpers import make_string_from_word_list
from user import set_user_league_team, user_exists
import constants


async def make_league_team_handler(db, message, client):

    word_parts = message.content.split(' ')

    team_role = int(word_parts[1])
    team_owner = message.mentions[0]
    team_name = make_string_from_word_list(word_parts, 3)

    role = await get_role_by_id(client, team_role)
    if not role:
        await message.channel.send('There is no role with that ID.')
        return
    
    owner_user = user_exists(db, team_owner.id)
    if not owner_user:
        await message.channel.send('That user is not registered.')
        return
    
    team_info_channel = client.get_channel(constants.TEAM_INFO_CHANNEL)
    player_string = team_owner.mention+' : Owner : 10 TPP'
    end_string = '\n--------------------------\nAvailable TPP: 90'
    new_team_message = await team_info_channel.send('**'+team_name+' Team Details**\nMembers:\n'+player_string+end_string)

    await give_role(team_owner, role, 'Make League Team')
    
    league_teams = db['leagueteams']

    new_team = {
        'team_name': team_name,
        'owner_id': team_owner.id,
        'members': [
            {
                'discord_id': team_owner.id,
                'is_owner': True,
                'is_admin': True,
                'role': 'Team Owner',
                'TPP': 10,
            }
        ],
        'team_info_msg_id': new_team_message.id,
        'team_role_id': team_role,
        'name_lower': team_name.lower(),
        'roster_lock': False
    }

    league_teams.insert_one(new_team)

    set_user_league_team(db, owner_user, team_name)

    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)
    await league_notifs_channel.send('New Team Created: "'+team_name+'". Owner is '+team_owner.mention)
    await message.channel.send('Team "'+team_name+'" was successfully created.')

