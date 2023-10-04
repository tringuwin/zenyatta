import copy
import random
import time
import discord
from common_messages import not_registered_response
import constants
from bracket import get_bracket_by_event_id, make_bracket_from_users
from rewards import change_passes, change_tokens
from user import get_user_passes, get_user_pickaxes, user_exists


def find_user_with_battle_tag(db, lower_tag):

    users = db['users']
    
    search_query = {"lower_tag": lower_tag}

    existing_user = users.find_one(search_query)

    if existing_user:
        return True
    else:
        return False
    
def create_or_update_battle_tag(db, battle_tag, lower_tag, discord_id):

    users = db['users']

    search_query = {"discord_id": int(discord_id)}

    existing_user = users.find_one(search_query)
    if existing_user:
        new_user = copy.deepcopy(existing_user)
        new_user['battle_tag'] = battle_tag
        new_user['lower_tag'] = lower_tag

        users.update_one({"discord_id": discord_id}, {"$set": {"battle_tag": battle_tag, "lower_tag": lower_tag}})
        print(users.find_one(search_query))
    else:

        new_user = {
            "battle_tag": battle_tag,
            "lower_tag": lower_tag,
            "discord_id": discord_id,
            "entries": [],
            "fun_fact": '',
            'teams': [],
            'passes': 1,
            'pickaxes': 0,
            'invited_valid': True,
            'level': 1,
            'xp': 0
        }
        print(new_user)
        users.insert_one(new_user)



def get_all_events(db):

    events = db['events']

    event_objects = events.find()
    return event_objects 




def create_event(db, event_id, event_name, max_players, pass_required, team_size, event_role_id, event_channel_id):

    events = db['events']
    needs_pass = False
    if pass_required == '1':
        needs_pass = True

    new_event = {
        "event_id": event_id,
        "event_name": event_name,
        "max_players": int(max_players),
        "spots_filled": 0,
        "entries": [],
        "requests": [],
        'needs_pass': needs_pass,
        'team_size': int(team_size),
        'event_role_id': int(event_role_id),
        'event_channel_id': int(event_channel_id)
    }

    events.insert_one(new_event)

async def give_event_role(client, member_id):
    guild = client.get_guild(constants.GUILD_ID)
    role = guild.get_role(constants.EVENT_ROLE)

    if role is not None:
        member = guild.get_member(member_id)
        if member:
            await member.add_roles(role)



async def output_tokens(db, message):


    existing_user = user_exists(db, message.author.id)

    if existing_user:

        if "tokens" in existing_user:
            await message.channel.send("Your tokens: 🪙**"+str(existing_user['tokens'])+"**")
        else:
            users = db['users']
            users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"tokens": 0}})
            await message.channel.send("Your tokens: 🪙**0**")

    else:
        await not_registered_response(message)
        


async def output_passes(db, message):

    existing_user = user_exists(db, message.author.id)

    if existing_user:

        if "passes" in existing_user:
            await message.channel.send("Your Priority Passes: 🎟️**"+str(existing_user['passes'])+"**")
        else:
            users = db['users']
            users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"passes": 0}})
            await message.channel.send("Your Priority Passes: 🎟️**0**")
    
    else:
        await not_registered_response(message)

async def output_eggs(db, message):

    existing_user = user_exists(db, message.author.id)

    if existing_user:

        if "eggs" in existing_user:
            await message.channel.send("Your Eggs: 🥚**"+str(existing_user['eggs'])+"**")
        else:
            users = db['users']
            users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"eggs": 0}})
            await message.channel.send("Your Eggs: 🥚**0**")

    else:
        await not_registered_response(message)


async def output_pickaxes(db, message):

    existing_user = user_exists(db, message.author.id)

    if not existing_user:
        await not_registered_response(message)
        return
    
    user_pickaxes = get_user_pickaxes(existing_user)
    await message.channel.send('Your Pickaxes: ⛏️**'+str(user_pickaxes)+'**')




async def switch_matches(db, message, event_id, match1, match2):

    my_bracket = await get_bracket_by_event_id(db, event_id)

    if my_bracket:

        brackets = db['brackets']

        round1copy = copy.deepcopy(my_bracket['bracket'][0])
        match1copy = copy.deepcopy(round1copy[int(match1)])
        match2copy = copy.deepcopy(round1copy[int(match2)])
        round1copy[int(match1)] = match2copy
        round1copy[int(match2)] = match1copy

        my_bracket['bracket'][0] = round1copy
        brackets.update_one({"event_id": event_id}, {"$set": {"bracket": my_bracket['bracket']}})

        await message.channel.send('Matches moved.')
    else:
        await message.channel.send("Could not find a bracket with that event id.")