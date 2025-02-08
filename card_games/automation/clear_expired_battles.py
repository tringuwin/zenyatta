import time

async def clear_expired_battles(db, message):

    card_battles = db['card_battles']
    all_battles = card_battles.find()

    battles_deleted = 0

    current_time = time.time()
    for battle in all_battles:
        if battle['expire_time'] < current_time:
            card_battles.delete_one({'card_display': battle['card_display']})
            battles_deleted += 1

    await message.channel.send('Deleted '+str(battles_deleted)+' expired battles.')
