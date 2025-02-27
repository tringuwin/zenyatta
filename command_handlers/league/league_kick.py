
from api import remove_role
from common_messages import invalid_number_of_params
from context.context_helpers import get_league_notifs_channel_from_context, get_league_team_field_from_context, get_league_teams_collection_from_context
from discord_actions import get_role_by_id
from helpers import get_league_emoji_from_team_name
from league import update_team_info, validate_admin

async def league_kick_handler(db, message, client, context):

    word_list = message.content.split()
    if len(word_list) != 2:
        await invalid_number_of_params(message)
        return
    
    if len(message.mentions) < 1:
        await message.channel.send('Please mention the player to kick.')
        return
    
    is_admin, my_team, team_name, is_owner = await validate_admin(db, message, context)
    
    if not my_team:
        await message.channel.send("You're not on a league team... So you can't kick people... dumbass...")
        return

    team_members = my_team['members']

    if not is_admin:
        await message.channel.send('You are not an admin of this league team. Please ask the team owner to be an admin.')
        return
    
    member_to_find = message.mentions[0]
    at_member = None
    cur_index = 0
    kick_user_is_admin = False
    kick_user_is_owner = False

    for member in team_members:
        if member['discord_id'] == member_to_find.id:
            at_member = member
            if member['is_admin']:
                kick_user_is_admin = True
            if member['is_owner']:
                kick_user_is_owner = True
            break
        cur_index += 1

    if not at_member:
        await message.channel.send('That member is not part of your team.')
        return
    
    if kick_user_is_owner:
        await message.channel.send('The owner of the team cannot be kicked.')
        return
    
    if kick_user_is_admin and (not is_owner):
        await message.channel.send('Only the owner of a team can kick admins.')
        return

    final_members = []
    for member in my_team['members']:
        if member['discord_id'] != member_to_find.id:
            final_members.append(member)

    league_teams = get_league_teams_collection_from_context(db, context)
    league_teams.update_one({'team_name': team_name}, {"$set": {"members": final_members}})

    users = db['users']
    league_team_field = get_league_team_field_from_context(context)
    users.update_one({"discord_id": member_to_find.id}, {"$set": {league_team_field: 'None'}})
    role = await get_role_by_id(client, my_team['team_role_id'])
    if role:
        await remove_role(member_to_find, role, 'League Kick')

    league_notifs_channel = get_league_notifs_channel_from_context(client, context)

    team_emoji_string = get_league_emoji_from_team_name(team_name)

    await league_notifs_channel.send(team_emoji_string+' Team Update for '+team_name+": "+member_to_find.mention+" was kicked by "+message.author.mention)

    my_team['members'] = final_members
    await update_team_info(client, my_team, db, context)

    await message.channel.send("User was kicked from the league team.")