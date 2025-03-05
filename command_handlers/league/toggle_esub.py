

from common_messages import not_registered_response
from discord_actions import get_role_by_id
from user import get_user_esub, get_user_esub_roles, get_user_ranks, get_user_rivals_esub, get_user_rivals_rank, user_exists
import constants

RANK_TO_ESUB_VALUE = {

    'Rank_Bronze_Division_5': 1,
    'Rank_Bronze_Division_4': 1,
    'Rank_Bronze_Division_3': 1,
    'Rank_Bronze_Division_2': 1,
    'Rank_Bronze_Division_1': 1,

    'Rank_Silver_Division_5': 1,
    'Rank_Silver_Division_4': 1,
    'Rank_Silver_Division_3': 1,
    'Rank_Silver_Division_2': 1,
    'Rank_Silver_Division_1': 1,

    'Rank_Gold_Division_5': 1,
    'Rank_Gold_Division_4': 1,
    'Rank_Gold_Division_3': 1,
    'Rank_Gold_Division_2': 1,
    'Rank_Gold_Division_1': 1,

    'Rank_Platinum_Division_5': 1,
    'Rank_Platinum_Division_4': 1,
    'Rank_Platinum_Division_3': 1,
    'Rank_Platinum_Division_2': 1,
    'Rank_Platinum_Division_1': 1,

    'Rank_Diamond_Division_5': 1,
    'Rank_Diamond_Division_4': 1,
    'Rank_Diamond_Division_3': 1,
    'Rank_Diamond_Division_2': 1,
    'Rank_Diamond_Division_1': 1,

    'Rank_Master_Division_5': 0,
    'Rank_Master_Division_4': 0,
    'Rank_Master_Division_3': 0,
    'Rank_Master_Division_2': 0,
    'Rank_Master_Division_1': 0,

    'Rank_GrandMaster_Division_5': 0,
    'Rank_GrandMaster_Division_4': 0,
    'Rank_GrandMaster_Division_3': 0,
    'Rank_GrandMaster_Division_2': 0,
    'Rank_GrandMaster_Division_1': 0,

    'Rank_Champ Division_5': 0,
    'Rank_Champ Division_4': 0,
    'Rank_Champ Division_3': 0,
    'Rank_Champ Division_2': 0,
    'Rank_Champ Division_1': 0,

}

DIV_TO_ROLE_ID = {

    'tank_1': 1305667046742298634,
    'offense_1': 1305667076362604595,
    'support_1': 1305667121539452928,

    # 'tank_2': 1242984687920746496,
    # 'offense_2': 1242985420552142960,
    # 'support_2': 1242985681446506597,

    # 'tank_3': 1242984723777847417,
    # 'offense_3': 1242985492249837568,
    # 'support_3': 1242985767735660636,

    # 'tank_4': 1270116909634818060,
    # 'offense_4': 1270116996134080624,
    # 'support_4': 1270117048734974014,

}

def user_ranks_empty(user_ranks):
    return (user_ranks['tank']['tier'] == 'none') and (user_ranks['offense']['tier'] == 'none') and (user_ranks['support']['tier'] == 'none')



async def toggle_esub_overwatch(db, message, client, user):

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
            await message.channel.send('Your current ranks are not elligible to be an Emergency Sub. You must have ranks between Bronze 5 and Diamond 1 to qualify.')
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
            #final_string += '\n**'+sub_role.upper()+':** Division '+str(div_num)+' Emergency Sub'
            final_string += '\n'+sub_role.upper()+' Emergency Sub'

        await message.channel.send(final_string)
            
    else:

        user_esub_roles = get_user_esub_roles(user)
        for role_id in user_esub_roles:
            role = await get_role_by_id(client, role_id)
            if role:
                await message.author.remove_roles(role)

        users = db['users']
        users.update_one({'discord_id': user['discord_id']}, {'$set': {'esub': False, 'esub_roles': []}})

        await message.channel.send('You are no longer an Emergency Sub! You can turn it back on anytime.')



async def get_rivals_esub_role(client):

    role = await get_role_by_id(client, constants.ESUB_MARVEL_RIVALS_ROLE)
    return role


async def remove_rivals_esub(db, message, client, user):

    users = db['users']

    users.update_one({'discord_id': user['discord_id']}, {'$set': {'rivals_esub': False}})

    esub_role = await get_rivals_esub_role(client)
    await message.author.remove_roles(esub_role)

    await message.channel.send('You are no longer an Emergency Sub for Marvel Rivals! You can turn it back on anytime.')

async def add_rivals_esub(db, message, client, user):

    users = db['users']

    users.update_one({'discord_id': user['discord_id']}, {'$set': {'rivals_esub': True}})

    esub_role = await get_rivals_esub_role(client)
    await message.author.add_roles(esub_role)

    await message.channel.send('You are now an Emergency Sub for Marvel Rivals! You can turn it off anytime.')


RIVALS_BLOCKED_ESUB_RANKS = ['GM', 'C', 'E', 'O']

async def toggle_esub_rivals(db, message, client, user):

    user_rivals_esub = get_user_rivals_esub(user)

    if user_rivals_esub:
        await remove_rivals_esub(db, message, client, user)
    else:
        user_rivals_rank = get_user_rivals_rank(user)
        if not user_rivals_rank:
            await message.channel.send('You must verify your Rivals rank first before you can be an Emergency Sub. Please make a support ticket and show a screenshot of your rank to staff.')
            return
        
        if user_rivals_rank['prefix'] in RIVALS_BLOCKED_ESUB_RANKS:
            await message.channel.send('Your are ranked too high to be an emergency sub. Emergency subs must be ranked Diamond 1 or lower.')
            return
        
        await add_rivals_esub(db, message, client, user)
        
        



async def toggle_esub_handler(db, message, client, context):

    if (context != 'OW') and (context != 'MR'):
        await message.channel.send('This command is not ready yet for this league.')
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    if context == 'OW':
        await toggle_esub_overwatch(db, message, client, user)
    elif context == 'MR':
        await toggle_esub_rivals(db, message, client, user)
        
