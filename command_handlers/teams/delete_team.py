
from common_messages import invalid_number_of_params, not_registered_response
from events import remove_team_from_event
from getters.event_getters import get_event_by_id
from helpers import make_string_from_word_list
from mongo import get_all_events
from teams import get_in_events, get_team_by_name, get_team_invites, remove_team_invite, remove_user_from_team
from user import user_exists

async def delete_team(db, team, client):
    team_members = team['members']
    for member in team_members:
        user = user_exists(db, member)
        if user:
            await remove_user_from_team(db, user, team, client)

    for invite in get_team_invites(team):
        user = user_exists(db, invite)
        if user:
            await remove_team_invite(db, user, team['team_name'])

    # for event_id in get_in_events(team):
    #     event = get_event_by_id(db, event_id)
    #     if event:
    #         await remove_team_from_event(client, db, team, event)

    teams = db['teams']
    teams.delete_one({'team_name': team['team_name']})


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

    team_in_event = False

    team_name = team['team_name']
    all_events = get_all_events(db)
    for event in all_events:
        if event['team_size'] == team['team_size']:
            for entry in event['entries']:
                if entry == team_name:
                    team_in_event = True
                    break

    if team_in_event:
        await message.channel.send('This team cannot be deleted right now because it is registered for an event.')
        return

    await delete_team(db, team, client)

    await message.channel.send('Team was successfully deleted.')

