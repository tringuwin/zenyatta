
from context.context_helpers import get_league_teams_collection_from_context
from safe_send import safe_send


async def handle_lock(db, message, lock_val, context):

    word_parts = message.content.split()

    if len(word_parts) > 2:
        await safe_send(message.channel, 'Only 2 or less params')
        return
    
    league_teams = get_league_teams_collection_from_context(db, context)

    # toggle all
    if len(word_parts) == 1:
        league_teams.update_many({}, {'$set': {'roster_lock': lock_val}})
        await safe_send(message.channel, 'Lock for all teams set to '+str(lock_val))

    # toggle single team
    elif len(word_parts) == 2:

        team_name_lower = word_parts[1].lower()

        league_team = league_teams.find_one({'name_lower': team_name_lower})
        if not league_team:
            await safe_send(message.channel, 'Did not find that team name.')
            return
        
        league_teams.update_one({'name_lower': team_name_lower}, {'$set': {'roster_lock': lock_val}})

        await safe_send(message.channel, 'Lock for '+team_name_lower+' set to '+str(lock_val))
        



