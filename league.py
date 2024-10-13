
import constants
from discord_actions import get_guild
from helpers import get_constant_value
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
    'Phantoms': discord.Colour(0xaabdcc),
    'Sentinels': discord.Colour(0x401b7a),
    'Diamonds': discord.Colour(0x78f0da),
    'Legion': discord.Colour(0xff0d1a),
    'Lotus': discord.Colour(0xf891a2),
    'Deadlock': discord.Colour(0x000000),
    'Horizon': discord.Colour(0xdd4f36),
    'Monarchs': discord.Colour(0x5c0106),
}

def get_team_color_by_name(team_name):

    return team_name_to_color[team_name]

team_name_to_thumbnail = {
    'Polar': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725044418/Polar_rmvnhc.png',
    'Olympians': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725045969/Olympians_gyfg6t.png',
    'Eclipse': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725045969/Eclipse_kzs5us.png',
    'Saviors': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725046016/Saviors_dxlwwp.png',
    'Ragu': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1723413292/Ragu_zewfly.png',
    'Instigators': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725046014/Instigators_kxmca7.png',
    'Guardians': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725046055/Guardians_kuftxa.png',
    'Phoenix': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725045969/Phoenix_ofiart.png',
    'Fresas': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725046015/Fresas_cyy8jr.png',
    'Outliers': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725046014/Outliers_i6r7wp.png',
    'Celestials': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725046055/Celestials_vdiudm.png',
    'Saturn': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725046054/Saturn_nmx1pr.png',
    'Evergreen': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725046015/Evergreen_svlg1g.png',
    'Misfits': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725045999/Misfits_af9iur.png',
    'Hunters': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725045970/Hunters_qlenfv.png',
    'Angels': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1722880276/Angels_xsl8cj.png',
    'Diamonds': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725381856/Diamonds_mg3ter.png',
    'Phantoms': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1723919677/Phantoms_pffpsp.png',
    'Sentinels': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1724962139/Sentinels_a6ndm4.png',
    'Legion': 'https://res.cloudinary.com/dc8euoeya/image/upload/v1725049269/Legion_v1kzyb.png',
    'Lotus': '',
    'Deadlock': '',
    'Horizon': '',
    'Monarchs': '',
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

    league_season = get_constant_value(db, 'league_season')

    standings = db['standings']
    standings_obj = standings.find_one({'season': league_season})

    team_record = standings_obj['teams'][team_name]
    return 'W: '+str(team_record[0])+' L: '+str(team_record[1])