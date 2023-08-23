

from events import event_is_open, get_event_team_size
from mongo import get_all_events


async def events_handler(db, message):

    event_list = get_all_events(db)
    found = False
    none_string = "It looks like there's no events right now... Check back soon!"
    # await message.channel.send(none_string)
    # return

    final_string = ""

    for event in event_list:

        if not event_is_open(event):
            continue

        found = True
        event_full = False
        if (event['max_players'] == event['spots_filled']):
            join_string = "FULL"
            event_full = True
        else:
            join_string = "**"+str(event['max_players']-event['spots_filled'])+" Spots Remaining**"

        num_players = get_event_team_size(event)
        add_part = 'Players'
        if num_players > 1:
            add_part = 'Teams'

        final_string = final_string+"**["+event['event_id']+"]** "+event['event_name']+" : "+ str(event['max_players']) +" Total "+add_part+" : "+join_string+' : '
        
        if num_players == 1:
            final_string += '1 player per team'
        else:
            final_string += str(num_players)+' players per team'

        if ('needs_pass' in event) and (event['needs_pass']):
            final_string += ' : ***🎟️ PRIORITY PASS REQUIRED 🎟️***'

        if not event_full:
            if num_players == 1:
                final_string += "\n*To join this event enter the command* **!join "+event['event_id']+"**\n\n"
            else:
                final_string += "\n*To join this event enter the command* **!teamjoin "+event['event_id']+" [team name here]**\n\n"
        else:
            final_string += "\n\n"

    if found:
        await message.channel.send(final_string)
    else:
        await message.channel.send(none_string)