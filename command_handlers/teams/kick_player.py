
from common_messages import invalid_number_of_params, not_registered_response
from helpers import make_string_from_word_list
from safe_send import safe_send
from teams import get_team_by_name, remove_user_from_team, user_on_team, user_owns_team
from user.user import user_exists


async def kick_player_handler(db, message, client):
    
    word_list = message.content.split(' ')
    if len(word_list) < 3:
        await invalid_number_of_params(message)
        return 

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    team_name = make_string_from_word_list(word_list, 2)
    team = await get_team_by_name(db, team_name)
    if not team:
        await safe_send(message.channel, 'There is no team with that name.')
        return

    mentions = message.mentions
    if len(mentions) != 1:
        await safe_send(message.channel, 'Please mention one player to kick.')
        return
    
    kick_user = user_exists(db, mentions[0].id)
    if not kick_user:
        await safe_send(message.channel, 'That user is not on this team.')
        return

    if not user_on_team(team, kick_user['discord_id']):
        await safe_send(message.channel, 'That user is not on this team.')
        return

    if not user_owns_team(team, user['discord_id']):
        await safe_send(message.channel, 'You do not own this team.')
        return

    await remove_user_from_team(db, kick_user, team, client)

    await safe_send(message.channel, 'Player was successfully kicked.')
