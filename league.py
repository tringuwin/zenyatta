
import constants
from discord_actions import get_guild
from user import get_league_invites, get_league_team, user_exists
import discord

async def validate_admin(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        return None, None, None, None
    
    user_team = get_league_team(user)
    if user_team == "None":
        return None, None, None, None

    league_teams = db['leagueteams']
    my_team = league_teams.find_one({'team_name': user_team})
    if not my_team:
        return None, None, None, None

    is_admin = False
    team_members = my_team['members']
    for member in team_members:
        if member['discord_id'] == user['discord_id'] and member['is_admin']:
            is_admin = True
            break

    is_owner = False
    if my_team['owner_id'] == user['discord_id']:
        is_owner = True

    return is_admin, my_team, my_team['team_name'], is_owner


team_name_to_color = {
    'Polar': discord.Colour(0x00c9eb),
    'Olympians': discord.Colour(0xf9c429),
    'Eclipse': discord.Colour(0x005fe8),
    'Saviors': discord.Colour(0x771da7),
    'Ragu': discord.Colour(0xE02814),
    'Instigators': discord.Colour(0x0c0c0c),
    'Guardians': discord.Colour(0xeb34d1),
    'Phoenix': discord.Colour(0xfc633d),
    'Fresas': discord.Colour(0xc33d3c),
    'Outliers': discord.Colour(0x1d0035)
}

team_name_to_thumbnail = {
    'Polar': 'https://i.imgur.com/mkbwgaD.png',
    'Olympians': 'https://i.imgur.com/rx8y0DM.png',
    'Eclipse': 'https://i.imgur.com/yuKFoDF.png',
    'Saviors': 'https://i.imgur.com/nrjx29Z.png',
    'Ragu': 'https://i.postimg.cc/5y2cSTFg/RAGU-FINAL-file.png',
    'Instigators': 'https://i.postimg.cc/mD8dSq2Y/Instigators.png',
    'Guardians': 'https://i.postimg.cc/zf2gmRXm/Guardians.png',
    'Phoenix': '',
    'Fresas': '',
    'Outliers': ''
}

async def update_team_info(client, team, db):

    team_message_id = team['team_info_msg_id']
    team_info_channel = client.get_channel(constants.TEAM_INFO_CHANNEL)

    info_message = await team_info_channel.fetch_message(team_message_id)

    guild = await get_guild(client)

    available_tpp = 100
    embed = discord.Embed(title=team['team_name'].upper()+' TEAM DETAILS', color=team_name_to_color[team['team_name']])
    embed.set_thumbnail(url=team_name_to_thumbnail[team['team_name']])

    for member in team['members']:
        print('member')

        try:
            guild_member = await guild.fetch_member(member['discord_id'])
        except discord.NotFound:
            guild_member = None

        member_mention = '[User not found]'
        if guild_member:
            member_mention = guild_member.mention

        member_battle_tag = '[Battle Tag Not Found]'
        user = user_exists(db, member['discord_id'])
        if user:
            member_battle_tag = user['battle_tag'].split('#')[0]

        name_string = member_battle_tag+' - '+member['role']

        value_string = ''
        if member['is_owner']:
            value_string = '👑 | '
        elif member['is_admin']:
            value_string = '🛡️ | '

        value_string += member_mention+' | '+str(member['TPP'])+' TPP'

        available_tpp -= member['TPP']

        embed.add_field(name=name_string, value=value_string, inline=False)

    embed.set_footer(text='Available TPP: '+str(available_tpp))

    await info_message.edit(embed=embed, content='')


def remove_league_invite(user, team_name, db):

    league_invites = get_league_invites(user)
    final_invites = []

    for invite in league_invites:
        if invite != team_name:
            final_invites.append(invite)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_invites": final_invites}})


def user_admin_on_team(user_id, league_team):

    for member in league_team['members']:

        if member['discord_id'] == user_id:
            if member['is_admin']:
                return True
            else:
                return False

    return False
