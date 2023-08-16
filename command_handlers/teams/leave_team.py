
from common_messages import invalid_number_of_params, not_registered_response
from teams import get_team_by_name, make_team_name_from_word_list, remove_user_from_team, user_on_team
from user import user_exists


async def leave_team_handler(db, message):
    
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

    if not user_on_team(team, user['discord_id']):
        await message.channel.send('You are not on this team.')
        return

    if team['creator_id'] == user['discord_id']:
        await message.channel.send('You are the creator of this team. Please delete the team instead of leaving.')
        return

    await remove_user_from_team(db, user, team)

    await message.channel.send('You have successfully left the team.')