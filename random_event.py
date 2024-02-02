import time
import constants
from discord_actions import get_guild
from rewards import change_tokens
from user import user_exists

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
    event_msg = await chat_channel.send('🎁 A RANDOM PRESENT HAS SPAWNED! CLICK THE KEY FIRST TO OPEN IT!🎁')
    
    random_event['last_event'] = current_time
    random_event['event_msg_id'] = event_msg.id
    random_event['claimed'] = 0

    db_constants.update_one({"name": 'random_event'}, {"$set": {"last_event": random_event['last_event'], "event_msg_id": random_event['event_msg_id'], "claimed": random_event['claimed']}})

    await event_msg.add_reaction('🔑')


async def react_to_event(db, client, message_id, member):

    db_constants = db['constants']
    random_event = db_constants.find_one({'name': 'random_event'})

    # check it's the event message
    if not (random_event['event_msg_id'] == message_id):
        return

    # check that hasn't been claimed
    if random_event['claimed'] == 1:
        return 

    # check that user is registered
    guild = await get_guild(client)
    chat_channel = guild.get_channel(constants.CHAT_CHANNEL)

    user = user_exists(db, member)
    if not user:
        await chat_channel.send(member.mention+" You're not registered yet. Please register before trying to claim a gift.")
        return
    
    db_constants.update_one({"name": 'random_event'}, {"$set": {"claimed": 1}})

    await chat_channel.send(member.mention+" You opened the present first! You won **100 Tokens!!** 🪙")
    await change_tokens(db, user, 100)