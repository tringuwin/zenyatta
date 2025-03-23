
from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from discord_actions import get_guild, get_member_by_id
from helpers import make_string_from_word_list
from league_helpers.give_member_admin_role import give_member_admin_role
from league_helpers.remove_member_admin_role import remove_member_admin_role
from user import get_league_team_with_context, user_exists


async def change_team_owner_handler(client, db, message, context):

    word_parts = message.content.split()
    if len(word_parts) < 3:
        await invalid_number_of_params(message)
        return
    
    league_teams = get_league_teams_collection_from_context(db, context)
    team_name = make_string_from_word_list(word_parts, 2)
    team_obj = league_teams.find_one({'team_name': team_name})
    if not team_obj:
        await message.channel.send('Could not find team "'+team_name+'"')
        return
    
    mentions = message.mentions
    if len(mentions) != 1:
        await message.channel.send('Please mention 1 user to make the team owner')
        return
    
    mention_member = mentions[0]
    user = user_exists(db, mention_member.id)
    if not user:
        await message.channel.send('That user is not registered')
        return
    
    user_league_team = get_league_team_with_context(user, context)
    if user_league_team != team_name:
        await message.channel.send('That user is not part of this team.')
        return
    
    old_owner_id = team_obj['owner_id']

    for member in team_obj['members']:
        if member['discord_id'] == old_owner_id:
            member['is_owner'] = False
            member['is_admin'] = False
        elif member['discord_id'] == mention_member.id:
            member['is_owner'] = True
            member['is_admin'] = True

    await give_member_admin_role(mention_member, context, client)

    guild = await get_guild(client)
    old_owner_member = await get_member_by_id(guild, old_owner_id)
    if old_owner_member:
        await remove_member_admin_role(old_owner_member, context, client)

    league_teams.update_one({'team_name': team_name}, {"$set": {"members": team_obj['members'], 'owner_id': mention_member.id}})

    await message.channel.send('League Team owner changed')


