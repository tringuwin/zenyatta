
from events import get_event_by_id
from helpers import make_string_from_word_list


async def del_team_from_event_handler(db, message):

    word_list = message.content.split()
    if len(word_list) < 2: 
        await message.channel.send('Not enough parameters')
        return
    
    event_id = word_list[1]
    event = get_event_by_id(db, event_id)
    if not event:
        await message.channel.send('No event with that id')
        return

    team_name = make_string_from_word_list(word_list, 2)
    team_name_lower = team_name.lower()
    entries = event['entries']
    final_entries = []
    print(str(len(entries)))
    for entry in entries:
        if entry.lower() != team_name_lower:
            final_entries.append(entry)
    print(str(len(final_entries)))

    events = db['events']
    events.update_one({"event_id": event['event_id']}, {"$set": {"entries": final_entries, "spots_filled": len(final_entries)}})
    await message.channel.send('command done')