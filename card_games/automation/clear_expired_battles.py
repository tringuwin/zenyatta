import time
import constants
from discord_actions import get_guild, get_message_by_channel_and_id

async def clear_expired_battles(client, db, message):

    card_battles = db['card_battles']
    all_battles = card_battles.find()

    users = db['users']

    battles_deleted = 0

    current_time = time.time()
    for battle in all_battles:
        if battle['expire_time'] < current_time:
            
            user = users.find_one({'discord_id': battle['user_id']})
            user_battle_cards = user['battle_cards']
            if battle['card_display'] in user_battle_cards:
                user_battle_cards.remove(battle['card_display'])
                users.update_one({'discord_id': user['discord_id']}, {'$set': {'battle_cards': user_battle_cards}})

            battle_message = await get_message_by_channel_and_id(client, constants.CARD_BATTLE_CHANNEL, battle['message_id'])
            await battle_message.delete()

            card_battles.delete_one({'card_display': battle['card_display']})

            battles_deleted += 1

    await message.channel.send('Deleted '+str(battles_deleted)+' expired battles.')
