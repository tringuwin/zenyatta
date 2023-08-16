
from common_messages import invalid_number_of_params, not_registered_response
from teams import add_user_to_team, get_team_by_name, make_team_name_from_word_list, remove_team_invite, team_is_full, user_on_team
from user import get_user_invites, get_user_teams, user_exists, user_invited_to_team
import constants


async def accept_invite_handler(db, message):
    
    word_list = message.content.split(' ')
    if len(word_list) < 2:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    team_name = make_team_name_from_word_list(word_list, 1)
    
    team = await get_team_by_name(db, team_name)
    if not team:
        await message.channel.send('There is no team with that name.')
        return
    
    if not user_invited_to_team(team, user):
        await message.channel.send('You do not have an invite to join this team.')
        return

    user_teams = get_user_teams(user)
    if len(user_teams) >= constants.MAX_PLAYER_TEAMS:
        await message.channel.send('You are already on '+str(constants.MAX_PLAYER_TEAMS)+' teams which is the max allowed.')
        return
    
    if user_on_team(team, user['discord_id']):
        await message.channel.send('You are already on this team.')
        return

    if team_is_full(team):
        await remove_team_invite(db, user, team_name)
        await message.channel.send('This team is currently full')
        return

    await add_user_to_team(db, user, team)
    await remove_team_invite(db, user, team_name)

    await message.channel.send('You have successfully joined the team **'+team['team_name']+'**')

    