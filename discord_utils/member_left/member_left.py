

from command_handlers.league.update_team import update_team
from constants import ALL_LEAGUE_CONTEXTS
from context.context_helpers import get_league_team_field_from_context
from user.user import user_exists


async def member_left(payload, db, client):

    guild_user = payload.user
    user_id = guild_user.id
    
    db_user = user_exists(db, user_id)
    if db_user:

        for context in ALL_LEAGUE_CONTEXTS:

            league_team_constant = get_league_team_field_from_context(context)
            if league_team_constant in db_user and db_user[league_team_constant] != 'None':
                
                user_team = db_user[league_team_constant]
                users = db['users']
                users.update_one({'discord_id': user_id}, {'$set': {league_team_constant: 'None'}})

                await update_team(db, user_team, client, context)
                