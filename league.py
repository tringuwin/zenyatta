
import constants
from discord_actions import get_guild

async def update_team_info(client, team):

    team_message_id = team['team_info_msg_id']
    team_info_channel = client.get_channel(constants.TEAM_INFO_CHANNEL)

    info_message = await team_info_channel.fetch_message(team_message_id)

    final_string = '**'+team['team_name']+' Team Details**\nMembers:'

    guild = await get_guild(client)

    available_tpp = 100
    for member in team['members']:

        guild_member = await guild.fetch_member(member['discord_id'])
        member_string = '*User not found*'
        if guild_member:
            member_string = guild_member.mention

        member_string += ' : '+member['role']+' : '+str(member['TPP'])+' TPP'

        available_tpp -= member['TPP']
        final_string += '\n'+member_string

    final_string += '\n--------------------------\nAvailable TPP: '+str(available_tpp)

    await info_message.update(content=final_string)