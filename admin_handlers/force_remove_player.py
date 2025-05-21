from mongo import find_event_by_event_id


async def force_remove_player_handler(db, message):
    
    word_parts = message.content.split()

    event_id = word_parts[1]
    user_id = int(word_parts[2])

    event = find_event_by_event_id(db, event_id)
    if not event:
        await message.channel.send('Event with that ID not found.')
        return

    player_removed = False
    final_entries = []
    for entry in event['entries']:
        if entry != user_id:
            final_entries.append(entry)
        else:
            player_removed = True

    events.update_one({"event_id": event['event_id']}, {"$set": {"entries": final_entries, "spots_filled": len(final_entries)}})

    if player_removed:
        await message.channel.send('Player was removed.')
    else:
        await message.channel.send('Player was not found.')