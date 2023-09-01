import copy
import random
import time
import discord
import constants
from bracket import get_bracket_by_event_id, make_bracket_from_users
from events import get_event_by_id, get_event_team_size
from rewards import change_passes, change_tokens
from user import get_user_passes, user_exists


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
            'teams': []
        }
        print(new_user)
        users.insert_one(new_user)



def get_all_events(db):

    events = db['events']

    event_objects = events.find()
    return event_objects 




def create_event(db, event_id, event_name, max_players, pass_required, team_size, event_role_id):

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
        'event_role_id': int(event_role_id)
    }

    events.insert_one(new_event)


async def deny_user(db, discord_id, event_id, deny_reason, discord_client, message):

    existing_user = user_exists(db, discord_id)
    if existing_user:

        users = db['users']

        new_user = copy.deepcopy(existing_user)
        new_user_entries = new_user['entries']
        for entry in new_user_entries:
            if entry['event_id'] == event_id:
                entry['status'] = "Denied with the following reason: "+deny_reason
        users.update_one({"discord_id": discord_id}, {"$set": {"entries": new_user['entries']}})

        user = await discord_client.fetch_user(int(discord_id))
        if user:
            try:
                await user.send("Update for your request to join event "+event_id+": **You were denied with the following reason: "+deny_reason+"**\nWe encourage you to join future events!")
                await message.channel.send("The user was notified of their denial.")
            except discord.Forbidden:
                await message.channel.send('I was not able to DM the user.')
        else:
            await message.channel.send("I couldn't find any discord user with that discord ID.")

    else:
        await message.channel.send("I didn't find any registered user with that discord ID")

async def give_event_role(client, member_id):
    guild = client.get_guild(constants.GUILD_ID)
    role = guild.get_role(constants.EVENT_ROLE)

    if role is not None:
        member = guild.get_member(member_id)
        if member:
            await member.add_roles(role)

async def approve_user(db, discord_id, event_id, discord_client, message):

    existing_user = user_exists(db, discord_id)
    if existing_user:

        events = db['events']
        my_event = get_event_by_id(db, event_id)
        if my_event:

            new_event = copy.deepcopy(my_event)
            new_event['entries'].append(discord_id)
            events.update_one({"event_id": event_id}, {"$set": {"entries": new_event['entries']}})
            events.update_one({"event_id": event_id}, {"$set": {"spots_filled": new_event['spots_filled'] + 1}})
            print(get_event_by_id(db, event_id))

            users = db['users']
            new_user = copy.deepcopy(existing_user)
            new_user_entries = new_user['entries']
            for entry in new_user_entries:
                if entry['event_id'] == event_id:
                    entry['status'] = "Approved"
            users.update_one({"discord_id": discord_id}, {"$set": {"entries": new_user['entries']}})

            user = await discord_client.fetch_user(int(discord_id))
            if user:
                try:
                    await give_event_role(discord_client, int(discord_id))
                    await user.send("You're in! You were approved for participation in **event "+event_id+"**!! Make sure to keep up to date on information so you don't miss it!")
                    await message.channel.send("The user was notified of their approval.")
                except discord.Forbidden:
                    await message.channel.send('I was not able to DM the user.')
            else:
                await message.channel.send("I couldn't find any discord user with that discord ID.")
        else:
            await message.channel.send("I could not find an event with that ID.")

    else:
        await message.channel.send("I didn't find any registered user with that discord ID")



async def generate_bracket(db, message, event_id):
    
    event = get_event_by_id(db, event_id)
    if not event:
        await message.channel.send("I couldn't find any event with that ID.")
        return


    existing_bracket = await get_bracket_by_event_id(db, event_id)
    if existing_bracket:
        await message.channel.send("A bracket has already been generated for this event.")
        return
    
   
    brackets = db['brackets']

    round1 = event['entries'].copy()
    random.shuffle(round1)
    event_size = get_event_team_size(event)

    new_bracket = {
        "event_id": event_id,
        "bracket": await make_bracket_from_users(round1, db, event_size)
    }

    brackets.insert_one(new_bracket)

    await message.channel.send("Bracket has been created for event "+event_id)
    print(new_bracket)



async def output_tokens(db, message):


    existing_user = user_exists(db, message.author.id)

    if existing_user:

        if "tokens" in existing_user:
            await message.channel.send("Your tokens: 🪙**"+str(existing_user['tokens'])+"**")
        else:
            users = db['users']
            users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"tokens": 0}})
            await message.channel.send("Your tokens: 🪙**0**")


async def output_passes(db, message):

    existing_user = user_exists(db, message.author.id)

    if existing_user:

        if "passes" in existing_user:
            await message.channel.send("Your Priority Passes: 🎟️**"+str(existing_user['passes'])+"**")
        else:
            users = db['users']
            users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"passes": 0}})
            await message.channel.send("Your Priority Passes: 🎟️**0**")

async def output_eggs(db, message):

    existing_user = user_exists(db, message.author.id)

    if existing_user:

        if "eggs" in existing_user:
            await message.channel.send("Your Eggs: 🥚**"+str(existing_user['eggs'])+"**")
        else:
            users = db['users']
            users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"eggs": 0}})
            await message.channel.send("Your Eggs: 🥚**0**")





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