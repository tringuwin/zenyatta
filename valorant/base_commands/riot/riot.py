

import copy
from api import get_member, give_role
import constants
from helpers import make_string_from_word_list, valid_number_of_params
from safe_send import safe_send
from user.user import user_exists

def create_new_user_from_riot_id(db, riot_id, user_id):

    users = db['users']

    riot_id_lower = riot_id.lower()

    new_user = copy.deepcopy(constants.DEFAULT_BLANK_USER)
    new_user["riot_id"] = riot_id
    new_user["riot_id_lower"] = riot_id_lower
    new_user["discord_id"] = user_id

    users.insert_one(new_user)


def handle_riot_link_success(db, message, riot_id):

    users = db['users']
    existing_user = user_exists(db, message.author.id)

    if existing_user:

        users.update_one({'discord_id': message.author.id}, {'$set': {'riot_id': riot_id, 'riot_id_lower': riot_id.lower()}})

    else:
        create_new_user_from_riot_id(db, riot_id, message.author.id)




async def riot_link(db, message, client, user, riot_id):
    
    if len(riot_id) > 30:
        await safe_send(message.channel, 'The Riot ID you provided is not valid.')
        return
    
    if not ('#' in riot_id):
        await safe_send(message.channel, "The Riot ID you provided seems to be missing the # and part at the end. Please include that too.")
        return
    
    if riot_id[0] == '#':
        await safe_send(message.channel, 'Riot IDs cannot start with the "#" character. Please use this format: RiotID#1234')
        return
        
    lower_id = riot_id.lower()
    users = db['users']

    user_with_riot_id = users.find_one({'riot_id_lower': lower_id})

    if user_with_riot_id:
        if user_with_riot_id['discord_id'] == message.author.id:
            await safe_send(message.channel, "You've already linked this Riot ID.")
        else:
            await safe_send(message.channel, "That Riot ID has already been connected to a different discord account. Please contact staff if you need help.")
        return
    
    handle_riot_link_success(db, message, riot_id)

    guild = client.get_guild(constants.GUILD_ID)
    reg_role = guild.get_role(constants.REGISTERED_ROLE)
    member = get_member(guild, user.id, 'Riot ID Link')
    if member and reg_role:
        await give_role(member, reg_role, 'Riot ID Link')

    await safe_send(message.channel, "Success! Your Riot ID has been linked to the Spicy Esports server! (Please note: if you change your Riot ID please use the !riot command again to update it!)")


async def riot_handler(db, message, client):
    
    word_parts = message.content.split()
    riot_id = make_string_from_word_list(word_parts, 1)

    await riot_link(db, message, client, message.author, riot_id)