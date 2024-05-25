

from user import user_exists

async def contact_member_to_reg(member):

    pass

async def add_to_battle(db, member, battle_info):

    if not battle_info['reg_open']:
        return
    
    sign_ups = battle_info['sign_ups']
    if member.id in sign_ups:
        return
    
    user = user_exists(db, member.id)
    if not user:
        await contact_member_to_reg(member)
        return
    
    battle_info['sign_ups'].append(member.id)
    constants_db = db['constants']
    constants_db.update_one({"name": "battle"}, {"$set": {"value": battle_info}})

    


    