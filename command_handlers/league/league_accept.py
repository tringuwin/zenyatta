

from api import give_role
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_guild, get_role_by_id
from helpers import get_league_emoji_from_team_name, make_string_from_word_list
from league import has_username_for_game, remove_league_invite, update_team_info
from league_helpers import get_league_invites_with_context, get_league_notifs_channel, get_league_team_with_context, get_league_teams_collection
from user import get_user_div, get_user_team_swaps, user_exists
import constants
from datetime import datetime
import pytz

def match_day_soft_lock():
    # Get the current time in EST
    est = pytz.timezone('America/New_York')
    current_time = datetime.now(est)
    
    # Define the start and end times
    start_time = current_time.replace(hour=15, minute=45, second=0, microsecond=0)
    end_time = current_time.replace(hour=21, minute=0, second=0, microsecond=0)
    
    # Check if it's Saturday or Sunday
    if current_time.weekday() in [5, 6]:  # Saturday=5, Sunday=6
        # Check if current time is between 3:45 PM and 7:30 PM
        if start_time <= current_time <= end_time:
            return True
    return False


async def league_accept_handler(db, message, client, context):

    word_list = message.content.split()
    if len(word_list) < 2:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    user_league_team = get_league_team_with_context(user, context)
    if user_league_team != "None":
        await message.channel.send('You are already on a league team. Please leave that team before joining another team. Use the command **!leagueleave** to leave your current team.')
        return
    
    if constants.SEASON_ACTIVE and match_day_soft_lock():
        await message.channel.send('Players are not allowed to join teams from 3:45 PM EST to 9:00 PM EST on SOL match days. Please try again later.')
        return
    
    team_name_to_join = make_string_from_word_list(word_list, 1)
    team_name_lower = team_name_to_join.lower()
    user_invites = get_league_invites_with_context(user, context)

    found_team = False
    for invite in user_invites:
        if invite.lower() == team_name_lower:
            found_team = True
            break

    if not found_team:
        await message.channel.send('You do not have a team invite from the team "'+team_name_to_join+'". Please check the spelling of the team name.')
        return
    
    league_teams = get_league_teams_collection(db, context)
    league_team = league_teams.find_one({'name_lower': team_name_lower})
    real_team_name = league_team['team_name']

    if league_team['roster_lock']:
        await message.channel.send('This team currently has a roster lock (maybe because they are in the play-offs). Please try joining this team after the lock is removed.')
        return

    if len(league_team['members']) >= 25:
        await message.channel.send('This League Team already has 25 players, which is the maximum allowed. Please contact an admin of this team if you think this is a mistake.')
        return
    
    if not has_username_for_game(user, context):
        if context == 'OW':
            await message.channel.send('Please link your battle tag before joining an Overwatch team. Use the command **!battle BattleTagHere#1234** to do this.')
        elif context == 'MR':
            await message.channel.send('Please link your Marvel Rivals username before joining a Marvel Rivals team. Use the command **!username UsernameHere** to do this.')
        return

    
    # season_active = False
    # team_swaps = 0
    # div_joined = 0
    # if constants.SEASON_ACTIVE:
        
    #     season_active = True

    #     # check if they have enough swaps
    #     team_swaps = get_user_team_swaps(user)
    #     if team_swaps < 1:
    #         await message.channel.send('You have already joined a team 3 times this season, which is the maximum allowed in one season.')
    #         return

    #     # check if they can move divs
    #     user_div = get_user_div(user)
    #     if (user_div != league_team['div']):

    #         if user_div != 0:
    #             await message.channel.send('You are division locked for the rest of this season. You can only join teams in Division '+str(user_div)+' until the season ends.')
    #             return
    #         else:
    #             div_joined = league_team['div']
    

    remove_league_invite(user, real_team_name, db, context)
    users = db['users']

    update_obj = {"league_team": real_team_name} if context == 'OW' else {'rivals_league_team': real_team_name}
    # if season_active:
    #     if div_joined != 0:
    #         update_obj = {"league_team": real_team_name, 'team_swaps': team_swaps - 1, 'user_div': div_joined}
    #     else:
    #         update_obj = {"league_team": real_team_name, 'team_swaps': team_swaps - 1}

    users.update_one({"discord_id": user['discord_id']}, {"$set": update_obj})


    league_team['members'].append(
        {
            'discord_id': user['discord_id'],
            'is_owner': False,
            'is_admin': False,
            'role': '[No Role Yet]',
            'TPP': 0,
        }
    )

    league_teams.update_one({'team_name': real_team_name}, {"$set": {"members": league_team['members']}})

    role = await get_role_by_id(client, league_team['team_role_id'])
    if role:
        await give_role(message.author, role, 'League Accept')

    await update_team_info(client, league_team, db, context)

    league_notifs_channel = get_league_notifs_channel(client, context)

    team_emoji_string = get_league_emoji_from_team_name(real_team_name)
    
    await league_notifs_channel.send(team_emoji_string+' User '+message.author.mention+' has joined the team "'+real_team_name+'".')
    # if div_joined != 0:
    #     await message.channel.send('You have successfully joined this team! You are now locked in **Division '+str(div_joined)+'** for the rest of this season.')
    # else:
    await message.channel.send('You have successfully joined this team!')


