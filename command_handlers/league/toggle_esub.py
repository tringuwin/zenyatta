

from common_messages import not_registered_response
from discord_actions import get_role_by_id
from user import get_user_esub, get_user_esub_roles, get_user_ranks, user_exists


RANK_TO_ESUB_VALUE = {

    'Rank_Bronze_Division_5': 0,
    'Rank_Bronze_Division_4': 0,
    'Rank_Bronze_Division_3': 0,
    'Rank_Bronze_Division_2': 0,
    'Rank_Bronze_Division_1': 0,

    'Rank_Silver_Division_5': 4,
    'Rank_Silver_Division_4': 4,
    'Rank_Silver_Division_3': 4,
    'Rank_Silver_Division_2': 4,
    'Rank_Silver_Division_1': 4,

    'Rank_Gold_Division_5': 4,
    'Rank_Gold_Division_4': 4,
    'Rank_Gold_Division_3': 4,
    'Rank_Gold_Division_2': 3,
    'Rank_Gold_Division_1': 3,

    'Rank_Platinum_Division_5': 3,
    'Rank_Platinum_Division_4': 3,
    'Rank_Platinum_Division_3': 3,
    'Rank_Platinum_Division_2': 2,
    'Rank_Platinum_Division_1': 2,

    'Rank_Diamond_Division_5': 2,
    'Rank_Diamond_Division_4': 2,
    'Rank_Diamond_Division_3': 2,
    'Rank_Diamond_Division_2': 1,
    'Rank_Diamond_Division_1': 1,

    'Rank_Master_Division_5': 1,
    'Rank_Master_Division_4': 1,
    'Rank_Master_Division_3': 1,
    'Rank_Master_Division_2': 0,
    'Rank_Master_Division_1': 0,

    'Rank_GrandMaster_Division_5': 0,
    'Rank_GrandMaster_Division_4': 0,
    'Rank_GrandMaster_Division_3': 0,
    'Rank_GrandMaster_Division_2': 0,
    'Rank_GrandMaster_Division_1': 0,

}

DIV_TO_ROLE_ID = {

    'tank_1': 1242984652134813717,
    'offense_1': 1242985354106114058,
    'support_1': 1242985545655648306,

    'tank_2': 1242984687920746496,
    'offense_2': 1242985420552142960,
    'support_2': 1242985681446506597,

    'tank_3': 1242984723777847417,
    'offense_3': 1242985492249837568,
    'support_3': 1242985767735660636,

    'tank_4': 1270116909634818060,
    'offense_4': 1270116996134080624,
    'support_4': 1270117048734974014,

}

def user_ranks_empty(user_ranks):


    return (user_ranks['tank']['tier'] == 'none') and (user_ranks['offense']['tier'] == 'none') and (user_ranks['support']['tier'] == 'none')


async def toggle_esub_handler(db, message, client):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_esub = get_user_esub(user)
    user_ranks = get_user_ranks(user)
    ranks_empty = user_ranks_empty(user_ranks)

    if (not user_esub) and ranks_empty:
        await message.channel.send('You do not have any ranks set currently. To verify your ranks, use the command **!verifyranks**')
        return
    
    if not user_esub:

        e_sub_ranks = {}

        for rank in user_ranks:
            rank_data = user_ranks[rank]
            if rank_data['tier'] == 'none':
                continue
            rank_string = rank_data['tier']+'_'+rank_data['div']
            rank_num = RANK_TO_ESUB_VALUE[rank_string]
            if rank_num == 0:
                continue
            e_sub_ranks[rank] = rank_num

        if len(e_sub_ranks) == 0:
            await message.channel.send('Your current ranks are not elligible to be an Emergency Sub.')
            return
        
        role_ids = []
        for sub_role in e_sub_ranks:
            role_key = sub_role+'_'+str(e_sub_ranks[sub_role])
            role_id = DIV_TO_ROLE_ID[role_key]
            role_ids.append(role_id)
            role = await get_role_by_id(client, role_id)
            await message.author.add_roles(role)

        users = db['users']
        users.update_one({'discord_id': user['discord_id']}, {'$set': {'esub': True, 'esub_roles': role_ids}})

        final_string = 'You have been given the following Emergency Sub roles:'
        for sub_role in e_sub_ranks:
            div_num = e_sub_ranks[sub_role]
            final_string += '\n**'+sub_role.upper()+':** Division '+str(div_num)+' Emergency Sub'

        await message.channel.send(final_string)
            
    else:

        user_esub_roles = get_user_esub_roles(user)
        for role_id in user_esub_roles:
            role = await get_role_by_id(client, role_id)
            await message.author.remove_role(role)

        users = db['users']
        users.update_one({'discord_id': user['discord_id']}, {'$set': {'esub': False, 'esub_roles': []}})

        await message.channel.send('You are no longer an Emergency Sub! You can turn it back on anytime.')

