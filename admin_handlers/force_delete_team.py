
from command_handlers.teams.delete_team import delete_team
from helpers import make_string_from_word_list
from safe_send import safe_send
from teams import get_team_by_name


async def force_delete_team_handler(db, message, client):

    word_list = message.content.split()
    team_name = make_string_from_word_list(word_list, 1)

    team = await get_team_by_name(db, team_name)
    if not team:
        await safe_send(message.channel, 'Team with that name does not exist')
        return
    
    await delete_team(db, team, client)
    await safe_send(message.channel, 'Team was deleted')