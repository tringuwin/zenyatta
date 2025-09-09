from admin_handlers.force_remove_player.get_force_remove_player_params.get_force_remove_player_params import get_force_remove_player_params
from mongo import find_event_by_event_id, update_event_by_event_id
from safe_send import safe_send


async def force_remove_player_handler(db, message):

    event_id, user_id = get_force_remove_player_params(message.content)

    event = find_event_by_event_id(db, event_id)
    if not event:
        await safe_send(message.channel, 'Event with that ID not found.')
        return

    player_removed = False
    final_entries = []
    for entry in event['entries']:
        if entry != user_id:
            final_entries.append(entry)
        else:
            player_removed = True

    event_update = {"entries": final_entries, "spots_filled": len(final_entries)}
    update_event_by_event_id(db, event_id, event_update)

    if player_removed:
        await safe_send(message.channel, 'Player was removed.')
    else:
        await safe_send(message.channel, 'Player was not found.')