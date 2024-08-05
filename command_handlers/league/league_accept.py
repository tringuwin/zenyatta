

from api import give_role
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_guild, get_role_by_id
from helpers import make_string_from_word_list
from league import remove_league_invite, update_team_info
from user import get_league_invites, get_league_team, get_user_div, get_user_div_swap, get_user_team_swaps, user_exists
import constants

async def league_accept_handler(db, message, client):

    word_list = message.content.split()
    if len(word_list) < 2:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_league_team = get_league_team(user)
    if user_league_team != "None":
        await message.channel.send('You are already on a league team. Please leave that team before joining another team.')
        return
    
    team_name_to_join = make_string_from_word_list(word_list, 1)
    team_name_lower = team_name_to_join.lower()
    user_invites = get_league_invites(user)

    found_team = False
    for invite in user_invites:
        if invite.lower() == team_name_lower:
            found_team = True
            break

    if not found_team:
        await message.channel.send('You do not have a team invite from the team "'+team_name_to_join+'". Please check the spelling of the team name.')
        return
    
    league_teams = db['leagueteams']
    league_team = league_teams.find_one({'name_lower': team_name_lower})
    real_team_name = league_team['team_name']

    if league_team['roster_lock']:
        await message.channel.send('This team currently has a roster lock (maybe because they are in the play-offs). Please try joining this team after the lock is removed.')
        return

    if len(league_team['members']) >= 25:
        await message.channel.send('This League Team already has 25 players, which is the maximum allowed. Please contact an admin of this team if you think this is a mistake.')
        return
    
    season_active = False
    team_swaps = 0
    div_joined = 0
    if constants.SEASON_ACTIVE:
        
        season_active = True

        await message.channel.send('If you see this message something went very wrong, please notify staff.')

        # check if they have enough swaps
        team_swaps = get_user_team_swaps(user)
        if team_swaps < 1:
            await message.channel.send('You have already joined a team 3 times this season, which is the maximum allowed in one season.')
            return

        # check if they can move divs
        user_div = get_user_div(user)
        if (user_div != league_team['div']):

            if user_div != 0:
                await message.channel.send('You are division locked for the rest of this season. You can only join teams in Division '+str(user_div)+' until the season ends.')
                return
            else:
                div_joined = league_team['div']
    

    remove_league_invite(user, real_team_name, db)
    users = db['users']

    update_obj = {"league_team": real_team_name}
    if season_active:
        if div_joined != 0:
            update_obj = {"league_team": real_team_name, 'team_swaps': team_swaps - 1, 'user_div': div_joined}
        else:
            update_obj = {"league_team": real_team_name, 'team_swaps': team_swaps - 1}

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

    await update_team_info(client, league_team, db)

    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)

    guild = await get_guild(client)
    team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[real_team_name]
    team_emoji = guild.get_emoji(team_emoji_id)
    
    await league_notifs_channel.send(str(team_emoji)+' User '+message.author.mention+' has joined the team "'+real_team_name+'".')
    await message.channel.send('You have successfully joined this team!')


