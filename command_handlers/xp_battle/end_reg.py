

from xp_battles import init_player_pools


async def end_reg_handler(db, message):

    constants_db = db['constants']
    battle_obj = constants_db.find_one({'name': 'battle'})
    battle_info = battle_obj['value']

    number_sign_ups = len(battle_info['sign_ups'])
    if number_sign_ups < 9:
        await message.channel.send('There are only '+str(number_sign_ups)+' players signed up for the battle. We need at least 9 players to start.')
        return
    
    init_player_pools()