import random
import time
import constants
from discord_actions import get_guild
from rewards import change_tokens
from user import get_user_gems, user_exists

SECONDS_IN_A_HOUR = 3600


random_event_list = {

    ['Gem', 'purple', 'Ana Gave You a Nano Boost! **(:gempurple:)**'],
    ['Gem', 'blue', 'Baptiste Saved You with an Immortality Field! **(:gemblue:)**'],
    ['Gem', 'yellow', 'You rallied with Brigitte! **(:gemyellow:)**'],
    ['Gem', 'orange', 'Junkrat gave you some loot from his last Heist! **(:gemorange:)**'],
    ['Gem', 'red', 'Kiriko gave you something that the Fox Spirit found! **(:gemred:)**'],
    ['Gem', 'pink', 'Lifeweaver gave you a someone he made with light! **(:gempink:)**'],
    ['Gem', 'green', 'Lucio gave you a cool souvenir at his concert! **(:gemgreen:)**'],
    ['Gem', 'teal', 'Mei gave you somethign she found frozen in the ice! **(:gemteal:)**'],
    ['Gem', 'black', 'Pharah gave you something she found in Egypt! **(:gemblack:)**'],
    ['Gem', 'white', 'Mercy pocketed you! **(:gemwhite:)**'],

    ['Token', 100, 'You got a Nano-Cola from D.Va! **(🪙 100)**'],
    ['Token', 70, 'You took a trip to England to visit Tracer! **(🪙 70)**'],
    ['Token', 60, 'Torbjorn installed some turrets to protect your house! **(🪙 60)**'],
    ['Token', 50, 'Reinhardt gave you some cool armor! **(🪙 50)**'],
    ['Token', 45, 'Wrecking ball built you your own hamster ball! **(🪙 45)**'],
    ['Token', 40, 'Symmetra built you your own personal teleporter! **(🪙 40)**'],
    ['Token', 30, 'Sojourn promoted you to Captain! **(🪙 30)**'],
    ['Token', 25, 'Illari gave you your own Healing Pylon! **(🪙 25)**'],
    ['Token', 22, 'You meditated with Zenyatta! **(🪙 22)**'],
    ['Token', 20, 'Cassidy gave you some shooting lessons! **(🪙 20)**'],
    ['Token', 18, 'Soldier 76 grilled a steak for you! **(🪙 18)**'],
    ['Token', 15, 'Ashe let you borrow B.O.B! **(🪙 15)**'],
    ['Token', 12, 'Zarya taught you some weightlifting skills! **(🪙 12)**'],
    ['Token', 10, 'Winston gave you some Peanut Butter! **(🪙 10)**'],
    ['Token', 8, 'Sigma gave you a lesson in astrophysics!**(🪙 8)**'],
    ['Token', 5, 'Echo taught you a new skill! **(🪙 5)**'],
    ['Token', 3, 'Orisa gave you a ride on her back! **(🪙 3)**'],
    ['Token', 1, 'Bastion waved to you! **(🪙 1)**'],
    ['Token', -1, 'Mauga stepped on your toe... **(🪙 -1)**'],
    ['Token', -3, 'Junker Queen accidently stabbed you... **(🪙 -3)**'],
    ['Token', -4, 'Roadhog stole your wallet... **(🪙 -4)**'],
    ['Token', -5, 'Ramattra punched you... **(🪙 -5)**'],
    ['Token', -8, 'Sombra hacked your OW account and changed your Battle Tag to "MagicPants"... **(🪙 -8)**'],
    ['Token', -10, 'Reaper shot you in the back... **(🪙 -10)**'],
    ['Token', -12, "You stepped in Widowmaker's venom mine... **(🪙 -12)**"],
    ['Token', -15, 'Moira experimented on you... **(🪙 -15)**'],
    ['Token', -20, 'Doomfist punched you into a wall... **(🪙 -20)**'],
    ['Token', -25, 'Genji deflected your ult... **(🪙 -25)**'],
    ['Token', -30, 'Hanzo 1 shot you from accross the map... **(🪙 -30)**'],

}


async def try_random_event(db, client):
    print('trying random event')

    db_constants = db['constants']
    random_event = db_constants.find_one({'name': 'random_event'})

    last_event = random_event['last_event']

    current_time = time.time()
    if current_time - last_event < SECONDS_IN_A_HOUR:
        print('not long enough')
        return

    guild = await get_guild(client)
    chat_channel = guild.get_channel(constants.CHAT_CHANNEL)

    event_msg = await chat_channel.send('❗ A RANDOM EVENT HAS SPAWNED! REACT FIRST TO OPEN IT! ❗')
    
    random_event['last_event'] = current_time
    random_event['event_msg_id'] = event_msg.id
    random_event['claimed'] = 0

    db_constants.update_one({"name": 'random_event'}, {"$set": {"last_event": random_event['last_event'], "event_msg_id": random_event['event_msg_id'], "claimed": random_event['claimed']}})

    await event_msg.add_reaction('❗')


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

    user = user_exists(db, member.id)
    if not user:
        await chat_channel.send(member.mention+" You're not registered yet. Please register before trying to claim a gift.")
        return
    
    db_constants.update_one({"name": 'random_event'}, {"$set": {"claimed": 1}})

    chosen_random_event = random.choice(random_event_list)
    event_message = chosen_random_event[2]

    await chat_channel.send(member.mention+" "+event_message)

    if chosen_random_event[0] == 'Token':
        await change_tokens(db, user, chosen_random_event[1])
    else:
        users = db['users']
        gem_color = chosen_random_event[1]
        user_gems = get_user_gems(user)
        user_gems[gem_color] += 1

        users = db['users']
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"gems": user_gems}})