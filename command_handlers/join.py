
import constants
from common_messages import not_registered_response
from discord_actions import give_role_to_user, member_has_role
from events import add_user_to_event_entries, event_has_space, event_is_open, get_event_role_id, get_event_team_size
from getters.event_getters import get_event_by_id
from helpers import valid_number_of_params
from safe_send import safe_send
from user.user import add_event_entry_to_user, user_entered_event, user_exists

async def join_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await safe_send(message.channel, "Command was not in the correct format. Please enter '!join' followed by the id of the event you want to join.")
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    event_id = params[1]
    if user_entered_event(user, event_id):
        await safe_send(message.channel, "You've already joined this event.")
        return
    
    event = get_event_by_id(db, event_id)
    if not event:
        await safe_send(message.channel, "I didn't find any events with that event ID. Use the command **!events** to see the current events.")
        return
    
    if get_event_team_size(event) > 1:
        await safe_send(message.channel, 'This is a team event. Please use the **!teamjoin** command with a team of size '+str(event['team_size'])+". Example: **!teamjoin "+event_id+" Team Name Here**")
        return
    
    if not event_is_open(event):
        await safe_send(message.channel, 'This event is not currently open for registration.')
        return

    if not event_has_space(event):
        await safe_send(message.channel, 'It looks like this event is full. Use the command **!events** to see if there are any events with remaining spots.')
        return

    is_twitch_sub = member_has_role(message.author, constants.TWITCH_SUB_ROLE)
    if event['needs_sub']:
        if not is_twitch_sub:
            await safe_send(message.channel, 'This event is only open to Twitch Subscribers.')
            return

    await add_event_entry_to_user(db, user, event_id)
    await add_user_to_event_entries(db, user, event)
    event_role_id = get_event_role_id(event)
    await give_role_to_user(client, message.author, event_role_id)

    await safe_send(message.channel, "Success! You've joined this event!")