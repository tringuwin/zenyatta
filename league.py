
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
    'Guardians': discord.Colour(0xff2af5),
    'Phoenix': discord.Colour(0xf15a29),
    'Fresas': discord.Colour(0xf92446),
    'Outliers': discord.Colour(0x361c89),
    'Celestials': discord.Colour(0x00aff0),
    'Saturn': discord.Colour(0xffb816),
    'Evergreen': discord.Colour(0x074735),
    'Misfits': discord.Colour(0xc3db35),
    'Hunters': discord.Colour(0x41564e),
    'Angels': discord.Colour(0xfff395),
    'Phantoms': discord.Colour(0xededed),
    'Sentinels': discord.Colour(0x2c114f),
    'Diamonds': discord.Colour(0x78f0da),
    'Legion': discord.Colour(0x6e0002)
}

def get_team_color_by_name(team_name):

    return team_name_to_color[team_name]

team_name_to_thumbnail = {
    'Polar': 'https://i.imgur.com/mkbwgaD.png',
    'Olympians': 'https://i.imgur.com/rx8y0DM.png',
    'Eclipse': 'https://i.imgur.com/yuKFoDF.png',
    'Saviors': 'https://i.imgur.com/nrjx29Z.png',
    'Ragu': 'https://i.imgur.com/05qnVcs.png',
    'Instigators': 'https://i.imgur.com/A01wK9e.png',
    'Guardians': 'https://i.imgur.com/DiVg8j2.png',
    'Phoenix': 'https://i.imgur.com/6cRlZqo.png',
    'Fresas': 'https://i.imgur.com/a9pYmfw.png',
    'Outliers': 'https://i.imgur.com/1lN3aul.png',
    'Celestials': 'https://i.imgur.com/gbrlk7Q.png',
    'Saturn': 'https://i.imgur.com/UJaIlua.png',
    'Evergreen': 'https://i.imgur.com/k4wFF5R.png',
    'Misfits': 'https://i.imgur.com/Aauu5rq.png',
    'Hunters': 'https://i.imgur.com/HEeAJwK.png',
    'Angels': '',
    'Diamonds': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1721793187/Diamonds_q79bq9.png',
    'Phantoms': '',
    'Sentinels': '',
    'Legion': ''
}


async def make_team_description(client, team):

    if len(team['allies']) == 0 and len(team['rivals']) == 0:
        return ''

    guild = await get_guild(client)
    final_desc = ''

    has_allies = False

    if len(team['allies']) > 0:
        has_allies = True
        ally_string = 'Allies:'
        for ally in team['allies']:
            ally_emoji_id = constants.LEAGUE_TO_EMOJI_ID[ally]
            ally_emoji = guild.get_emoji(ally_emoji_id)
            ally_string += ' '+str(ally_emoji)+' '+ally

        final_desc += ally_string

    if len(team['rivals']) > 0:
        if has_allies:
            final_desc += '\n'

        rival_string = 'Rivals:'
        for rival in team['rivals']:
            rival_emoji_id = constants.LEAGUE_TO_EMOJI_ID[rival]
            rival_emoji = guild.get_emoji(rival_emoji_id)
            rival_string += ' '+str(rival_emoji)+' '+rival

        final_desc += rival_string
    
    return final_desc
        




async def update_team_info(client, team, db):

    team_message_id = team['team_info_msg_id']
    team_info_channel = client.get_channel(constants.TEAM_INFO_CHANNEL)

    info_message = await team_info_channel.fetch_message(team_message_id)

    guild = await get_guild(client)

    available_tpp = 100
    num_members_on_team = str(len(team['members']))
    embed_description = await make_team_description(client, team)
    embed = discord.Embed(title=team['team_name'].upper()+' TEAM DETAILS ('+num_members_on_team+'/25)', color=team_name_to_color[team['team_name']], description=embed_description)
    embed.set_thumbnail(url=team_name_to_thumbnail[team['team_name']])

    for member in team['members']:

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


def get_team_record_string(db, team_name):

    standings = db['standings']
    standings_obj = standings.find_one({'season': constants.LEAGUE_SEASON})

    team_record = standings_obj['teams'][team_name]
    return 'W: '+str(team_record[0])+' L: '+str(team_record[1])