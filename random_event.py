import time
import constants
from discord_actions import get_guild

SECONDS_IN_A_HOUR = 3600

async def try_random_event(db, client):

    db_constants = db['constants']
    random_event = db_constants.find_one({'name': 'random_event'})

    last_event = random_event['last_event']

    current_time = time.time()
    if current_time - last_event < SECONDS_IN_A_HOUR:
        return
    
    '🎁 A RANDOM PRESENT HAS SPAWNED! CLICK THE KEY FIRST TO OPEN IT! (this feature does not work yet) 🎁'

    guild = await get_guild(client)
    chat_channel = guild.get_channel(constants.CHAT_CHANNEL)
    event_msg = await chat_channel.send('🎁 A RANDOM PRESENT HAS SPAWNED! CLICK THE KEY FIRST TO OPEN IT! (this feature does not work yet) 🎁')
    
    random_event['last_event'] = current_time
    random_event['event_msg_id'] = event_msg.id
    random_event['claimed'] = 0

    db_constants.update_one({"name": 'raffle_total'}, {"$set": {"last_event": random_event['last_event'], "event_msg_id": random_event['event_msg_id'], "claimed": random_event['claimed']}})

    await event_msg.add_reaction('🗝️')


