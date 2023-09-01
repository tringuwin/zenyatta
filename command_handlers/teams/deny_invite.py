
from common_messages import invalid_number_of_params, not_registered_response
from helpers import make_string_from_word_list
from teams import get_team_by_name, remove_team_invite, user_invited_to_team
from user import user_exists


async def deny_invite_handler(db, message):
    
    word_list = message.content.split(' ')
    if len(word_list) < 2:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    team_name = make_string_from_word_list(word_list, 1)
    team = await get_team_by_name(db, team_name)
    if not team:
        await message.channel.send('There is no team with that name.')
        return

    if not user_invited_to_team(team, user):
        await message.channel.send('You are not invited to this team.')
        return

    await remove_team_invite(db, user, team_name)

    await message.channel.send('Team invite was successfully denied.')