
from common_messages import invalid_number_of_params, not_registered_response
from helpers import make_string_from_word_list
from teams import add_invite_to_team, get_team_by_name, invite_user_to_team, team_is_full, user_invited_to_team, user_on_team
from user import user_exists


async def invite_handler(db, message, is_admin):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    word_list = message.content.split(' ')
    if len(word_list) < 3:
        await invalid_number_of_params(message)
        return
    
    team_name = make_string_from_word_list(word_list, 2)
    team = await get_team_by_name(db, team_name)
    if not team:
        await message.channel.send('There is no team with that name.')
        return
    
    if team['creator_id'] != user['discord_id'] and (not is_admin):
        await message.channel.send('You are not the owner of this team.')
        return
    
    if team_is_full(team):
        await message.channel.send('This team is currently full.')
        return
    
    mentions = message.mentions
    if len(mentions) != 1:
        await message.channel.send('Please mention 1 player to invite to the team')
        return
    
    invited_member = mentions[0]
    invited_user = user_exists(db, invited_member.id)
    if not invited_user:
        await message.channel.send('That user is not registered. Please have them register with this command: **!battle BattleTagHere#1234**')
        return

    if user_on_team(team, invited_user['discord_id']):
        await message.channel.send('That user is already on this team.')
        return

    if user_invited_to_team(team, invited_user):
        await message.channel.send('This user has already been invited to this team.')
        return
    
    await invite_user_to_team(db, team, invited_user)
    add_invite_to_team(db, team, invited_user['discord_id'])
    await message.channel.send('User was successfully invited to the team! '+invited_member.mention+' to accept this invite, please say **!acceptinvite '+team['team_name']+'**')