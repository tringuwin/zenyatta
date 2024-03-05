import copy

import discord
import constants
import time

def user_exists(db, discord_id):
    
    users = db['users']

    search_query = {"discord_id": int(discord_id)}

    return users.find_one(search_query)

def get_user_by_tag(db, lower_tag):

    users = db['users']

    search_query = {"lower_tag": lower_tag}

    return users.find_one(search_query)


def get_user_tokens(user):

    if 'tokens' in user:
        return user['tokens']
    
    return 0

def get_user_passes(user):

    if 'passes' in user:
        return user['passes']
    
    return 0

def get_user_pickaxes(user):

    if 'pickaxes' in user:
        return user['pickaxes']
    
    return 0

def get_user_packs(user):

    if 'packs' in user:
        return user['packs']
    
    return 0

def get_user_tickets(user):

    if 'tickets' in user:
        return user['tickets']
    
    return 0

def get_last_sac(user):

    if 'last_sac' in user:
        return user['last_sac']
    
    return 0

def get_lvl_info(user):

    level = 1
    xp = 0
    if 'level' in user:
        level = user['level']
    if 'xp' in user:
        xp = user['xp']

    return level, xp



def get_role_id_by_level(level_num):
    role_id_index = level_num - 1
    return constants.LEVEL_ROLE_IDS[role_id_index]

def add_team_to_user(db, user, team_name):

    users = db['users']

    if not ('teams' in user):
        user['teams'] = []

    user['teams'].append(team_name)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"teams": user['teams']}})


def get_user_invites(user):
    
    if 'invites' in user:
        return user['invites']
    else:
        return []

def get_user_teams(user):

    if 'teams' in user:
        return user['teams']
    else:
        return []
    
    
def get_knows_gift(user):

    if 'knows_gift' in user:
        return user['knows_gift']
    else:
        return False
    
def get_last_gift(user):

    if 'last_gift' in user:
        return user['last_gift']

    else:
        return 0

    
def get_invited_valid(user):

    if 'invited_valid' in user:
        return user['invited_valid']
    else:
        return False
    
def get_user_gems(user):

    if 'gems' in user:
        return user['gems']
    else:
        return copy.deepcopy(constants.DEFAULT_GEMS)
    
def get_user_lootboxes(user):

    if 'lootboxes' in user:
        return user['lootboxes']
    else:
        return []
    
def get_sub_lootboxes(user):

    if 'sub_lootboxes' in user:
        return user['sub_lootboxes']
    else:
        return 0
    
def get_last_sub_box(user):

    if 'last_sub_box' in user:
        return user['last_sub_box']
    else:
        return 0

def get_league_team(user):
    if 'league_team' in user:
        return user['league_team']
    else:
        return 'None'
    
def get_league_invites(user):

    if 'league_invites' in user:
        return user['league_invites']
    else:
        return []
    
def get_gem_offer(user):

    if 'gem_offer' in user:

        offer = user['gem_offer']

        if (not offer) or offer == None:
            return None 

        current_time = time.time()

        if (current_time - offer['time_sent']) > 300:
            return None

        return user['gem_offer']
    else:
        return None
    
def get_fan_of(user):

    if 'fan_of' in user:
        return user['fan_of']
    return 'None'

def get_rival_of(user):

    if 'rival_of' in user:
        return user['rival_of']
    return 'None'

def get_last_token_shop(user):

    if 'last_token_shop' in user:
        return user['last_token_shop']
    
    return 0

def get_user_cards(user):

    if 'cards' in user:
        return user['cards']
    
    return []

def get_user_for_sale_cards(user):

    if 'for_sale_cards' in user:
        return user['for_sale_cards']
    
    return []

def get_user_ranks(user):

    if 'ranks' in user:
        return user['ranks']
    
    return {
        'tank': {
            'tier': 'none',
            'div': 'none'
        },
        'offense': {
            'tier': 'none',
            'div': 'none'
        },
        'support': {
            'tier': 'none',
            'div': 'none'
        },
    }
    
def toggle_off_gift_notify(db, user):

    users = db['users']

    users.update_one({"discord_id": user['discord_id']}, {"$set": {"gift_notify": False}})

def set_user_league_team(db, user, team):

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_team": team}})


def user_entered_event(user, event_id):

    user_entries = user['entries']
    for entry in user_entries:
        if entry['event_id'] == event_id:
            return True
        
    return False


async def add_event_entry_to_user(db, user, event_id):
    
    users = db['users']

    new_user = copy.deepcopy(user)
    entry_info = {
        "event_id": event_id,
        "status": "Not Reviewed",
    }
    new_user['entries'].append(entry_info)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"entries": new_user['entries']}})


async def notify_user_of_gift(member):

    pass


async def notify_user_of_gift(member, bot_coms_channel):
    try:
        # Try to send a DM
        await member.send('Your gift is ready in the Spicy OW server! Just say **!gift** here to claim! '+bot_coms_channel.jump_url)
    except discord.Forbidden:
        # If DM can't be sent, mention the member in the channel
        await bot_coms_channel.send(f'Your gift is ready, {member.mention}! (I tried to DM you but your privacy settings did not allow me to)')