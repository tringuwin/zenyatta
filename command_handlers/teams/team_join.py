
from common_messages import invalid_number_of_params, not_registered_response
from events import add_team_to_event, event_has_space, event_is_open, get_event_by_id, get_event_team_size, player_on_team_in_event, team_in_event
from helpers import make_string_from_word_list
from teams import get_team_by_name, team_is_full
from user import user_exists


async def team_join_handler(db, message):

    word_list = message.content.split(' ')
    if len(word_list) < 3:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    event_id = word_list[1]
    event = get_event_by_id(db, event_id)
    if not event:
        await message.channel.send('There is no event with that ID.')
        return

    if not event_is_open(event):
        await message.channel.send('This event is not currently open for registration.')
        return

    if not event_has_space(event):
        await message.channel.send('This event is full!')
        return

    team_name = make_string_from_word_list(word_list, 2)
    team = get_team_by_name(db, team_name)
    if not team:
        await message.channel.send('There is no team with that name.')
        return

    if not (team['creator_id'] == user['discord_id']):
        await message.channel.send('You do not own this team. Only the owner can join events.')
        return

    event_team_size = get_event_team_size(event)
    if event_team_size != team['team_size']:
        await message.channel.send('This team is not the correct size for this event. This event is only for teams of size '+str(event_team_size))
        return

    if not team_is_full(team):
        await message.channel.send('This team is not full! Only full teams can join events.')
        return

    if team_in_event(event, team):
        await message.channel.send('This team is already in this event.')
        return

    if await player_on_team_in_event(db, event, team):
        await message.channel.send('One or more players on this team is already participating in this event!')
        return

    await add_team_to_event(db, team, event)

    await message.channel.send('Success! This team has been registered for this event!')