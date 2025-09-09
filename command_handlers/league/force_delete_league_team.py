
from helpers import make_string_from_word_list
from safe_send import safe_send


async def force_delete_league_team_handler(db, message):
    
    word_parts = message.content.split()
    team_name = make_string_from_word_list(word_parts, 1)

    league_teams = db['leagueteams']
    team = league_teams.find_one({'team_name': team_name})
    if not team:
        await safe_send(message.channel, 'Team not found')
        return
    
    league_teams.delete_one({'team_name': team_name})
    await safe_send(message.channel, 'Team Deleted')