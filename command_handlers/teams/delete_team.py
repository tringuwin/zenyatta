
from common_messages import invalid_number_of_params, not_registered_response
from helpers import make_string_from_word_list
from teams import delete_team, get_team_by_name
from user import user_exists


async def delete_team_handler(db, message, client):
    
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

    if not (team['creator_id'] == user['discord_id']):
        await message.channel.send('You are not the owner of this team. Only the owner can delete the team.')
        return

    await delete_team(db, team, client)

    await message.channel.send('Team was successfully deleted.')

