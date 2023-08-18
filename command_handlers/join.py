


import discord
from common_messages import not_registered_response
from events import add_user_to_event_entries, event_has_space, get_event_by_id
from helpers import valid_number_of_params
from rewards import change_passes
import constants

from user import add_event_entry_to_user, get_user_passes, user_entered_event, user_exists


async def send_event_request_notif(message, event_id, discord_client, user):

    requests_channel_id = constants.EVENT_REQUESTS_CHANNEL
    target_channel = discord_client.get_channel(requests_channel_id)
    if target_channel:

        embed = discord.Embed(
            title = "Event Join Request"
        )
        embed.add_field(name='Event ID', value=event_id, inline=False)
        embed.add_field(name='Discord ID', value=str(user['discord_id']), inline=False)
        embed.add_field(name='Discord Name', value=message.author.name, inline=False)
        embed.add_field(name='Battle Tag', value=user['battle_tag'], inline=False)
        sent_message = await target_channel.send(embed=embed)
        await sent_message.add_reaction("✅")



async def join_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        message.channel.send("Command was not in the correct format. Please enter '!join' followed by the id of the event you want to join.")
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    event_id = params[1]
    if user_entered_event(user, event_id):
        await message.channel.send("It looks like you've already tried to join this event. To see the status of your join request for this event enter the command **!status "+event_id+"**")
        return
    
    event = get_event_by_id(db, event_id)
    if not event:
        await message.channel.send("I didn't find any events with that event ID. Use the command **!events** to see the current events.")
        return
    
    if not event_has_space(event):
        await message.channel.send('It looks like this event is full. Use the command **!events** to see if there are any events with remaining spots.')
        return
    
    if event['needs_pass']:
        if get_user_passes(user) < 1:
            await message.channel.send('This event requires a Priority Pass 🎟️ to join right now! Please get a Priority Pass first or wait until the event is open to everyone!')
            return
        else:
            await change_passes(db, user, -1)

    await add_event_entry_to_user(db, user, event_id)
    await add_user_to_event_entries(db, user, event)

    await message.channel.send("Success! You've joined this event!")

    await send_event_request_notif(message, event['event_id'], client, user)