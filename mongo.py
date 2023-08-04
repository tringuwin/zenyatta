import copy
import random
import discord
from discord.utils import get
from bracket import make_bracket_from_users


def find_user_with_battle_tag(db, lower_tag):

    users = db['users']
    
    search_query = {"lower_tag": lower_tag}

    existing_user = users.find_one(search_query)

    if existing_user:
        return True
    else:
        return False
    
def user_exists(db, discord_id):
    
    users = db['users']

    search_query = {"discord_id": int(discord_id)}

    return users.find_one(search_query)

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
            "entries": []
        }
        print(new_user)
        users.insert_one(new_user)


def get_event_by_id(db, event_id):

    events = db['events']

    search_query = {"event_id": event_id}

    return events.find_one(search_query)

def get_all_events(db):

    events = db['events']

    event_objects = events.find()
    return event_objects 

async def get_bracket_by_event_id(db, event_id):

    brackets = db['brackets']

    search_query = {"event_id": event_id}

    return brackets.find_one(search_query)


def create_event(db, event_id, event_name, max_players):

    events = db['events']

    new_event = {
        "event_id": event_id,
        "event_name": event_name,
        "max_players": int(max_players),
        "spots_filled": 0,
        "entries": [],
        "requests": []
    }

    events.insert_one(new_event)




async def try_join_event(db, message, event_id, discord_client):

    discord_id = message.author.id

    # ensure user is registered
    existing_user = user_exists(db, discord_id)
    print(existing_user)
    if existing_user:

        # check if user has already attempted to join this event
        user_entries = existing_user['entries']
        already_joined = False
        for entry in user_entries:
            if entry['event_id'] == event_id:
                already_joined = True
                break
        
        if already_joined:
            await message.channel.send("It looks like you've already tried to join this event. To see the status of your join request for this event enter the command **!status "+event_id+"**")

        else:

            # check if event exists / is full
            events = db['events']

            my_event = get_event_by_id(db, event_id)
            if my_event:

                if my_event['max_players'] == my_event['spots_filled']:
                    await message.channel.send('It looks like this event is full. Use the command **!events** to see if there are any events with remaining spots.')
                else:

                    users = db['users']

                    # add event entry to user
                    new_user = copy.deepcopy(existing_user)
                    entry_info = {
                        "event_id": event_id,
                        "status": "Not Reviewed",
                    }
                    new_user['entries'].append(entry_info)
                    users.update_one({"discord_id": discord_id}, {"$set": {"entries": new_user['entries']}})

                    # add user to event
                    new_event = copy.deepcopy(my_event)
                    request_info = {
                        "discord_id": discord_id,
                        "battle_tag": existing_user['battle_tag']
                    }
                    new_event['requests'].append(request_info)
                    events.update_one({"event_id": event_id}, {"$set": {"requests": new_event['requests']}})

                    requests_channel_id = 1131281041454280784
                    target_channel = discord_client.get_channel(requests_channel_id)
                    if target_channel:

                        embed = discord.Embed(
                            title = "Event Join Request"
                        )
                        embed.add_field(name='Event ID', value=event_id, inline=False)
                        embed.add_field(name='Discord ID', value=str(discord_id), inline=False)
                        embed.add_field(name='Discord Name', value=message.author.name, inline=False)
                        embed.add_field(name='Battle Tag', value=existing_user['battle_tag'], inline=False)
                        sent_message = await target_channel.send(embed=embed)
                        await sent_message.add_reaction("✅")

                    await message.channel.send("Success! You've made a request to join this event. Your request will be manually verified and you will be given a special role in the discord server if you are accepted. Enter the command **!status "+ event_id+"** at any time to see the status of your join request.")

            else:
                await message.channel.send("I didn't find any events with that event ID. Use the command **!events** to see the current events.")

    else:
        await message.channel.send("You need to connect your Battle Tag to your discord account before you can join an event. Enter the command **!register** for more info.")


async def event_status(db, message, event_id): 

    discord_id = message.author.id

    existing_user = user_exists(db, discord_id)
    if existing_user:
        user_entries = existing_user['entries']
        entry_found = False
        for entry in user_entries:
            if entry['event_id'] == event_id:
                await message.channel.send("Status for join request for event "+event_id+": **"+entry['status']+"**")
                entry_found = True
        if not entry_found:
            await message.channel.send("I couldn't find any event with ID '"+event_id+"'. Enter the command **!events** for a list of current events.")
    else:
        await message.channel.send("It looks like you have not connected your Battle Tag to your discord account yet. Please enter the command **!register** for more info.")

    

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

    if event:

        existing_bracket = await get_bracket_by_event_id(db, event_id)
        if existing_bracket:
            await message.channel.send("A bracket has already been generated for this event.")
        else:
            brackets = db['brackets']

            round1 = event['entries'].copy()
            random.shuffle(round1)

            new_bracket = {
                "event_id": event_id,
                "bracket": await make_bracket_from_users(round1, db)
            }

            brackets.insert_one(new_bracket)

            await message.channel.send("Bracket has been created for event "+event_id)

    else:
        await message.channel.send("I couldn't find any event with that ID.")


async def output_tokens(db, message):


    existing_user = user_exists(db, message.author.id)

    if existing_user:

        if "tokens" in existing_user:
            await message.channel.send("Your tokens: 🪙**"+str(existing_user['tokens'])+"**")
        else:
            users = db['users']
            users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"tokens": 0}})
            await message.channel.send("Your tokens: 🪙**0**")


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
        brackets.update_one({"event_id": event_id}, {"$set": {"bracket": my_bracket}})

        await message.channel.send('Matches moved.')
    else:
        await message.channel.send("Could not find a bracket with that event id.")