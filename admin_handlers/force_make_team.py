
from teams import add_user_to_team, get_team_by_name, make_team
from user import user_exists


async def force_make_team_handler(db, message, client):

    parts = message.content.split('|')

    if len(parts) < 4:
        await message.channel.send('Not enough parameters')
        return
    
    parts.pop(0)
    team_name = parts.pop(0)

    missing_user = 0
    for member_id in parts:
        user = user_exists(db, member_id)
        if not user:
            missing_user = member_id
            return
        
    if missing_user != 0:
        await message.channel.send('Did not find any user with id: '+str(missing_user))
        return

    team_owner_user = user_exists(db, parts[0])
    make_team(db, team_owner_user, len(parts), team_name)
    parts.pop(0)

    team_obj = get_team_by_name(db, team_name)
    for member_id in parts:
        user_obj = user_exists(db, member_id)
        add_user_to_team(db, user_obj, team_obj, client)



    



