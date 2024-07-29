
import discord

async def help_league_admin_handler(message):

    help_embed = discord.Embed(title='List of league team admin commands:')
    help_embed.add_field(name='!helpally', value='Show a list of league team admin commands related to League Team Allies and Rivals.', inline=False)
    help_embed.add_field(name='!leagueinvite @User', value='Admin command to invite a user to your league team', inline=False)
    help_embed.add_field(name='!leaguecancelinvite @User', value="Admin command to cancel a user's pending invite to your team.", inline=False)
    help_embed.add_field(name='!changetpp username [tpp number]', value='Admin command to change the TPP of a player on your league team.', inline=False)
    help_embed.add_field(name='!changerole @Player [role info]', value='Admin command to change the role of a player on your league team.', inline=False)
    help_embed.add_field(name='!maketeamadmin @Player', value='Owner command to make a member of your league team an admin.', inline=False)
    help_embed.add_field(name='!removeteamadmin @Player', value='Owner command to remove admin role from a member of your league team.', inline=False)
    help_embed.add_field(name='!leaguekick @Player', value='Admin command to kick a player from your league team.', inline=False)
    help_embed.add_field(name='!setappslink', value='Admin command to set the link for a Google Form that players can use to apply to the team.', inline=False)
    help_embed.add_field(name='!toggleapps', value='Admin command to set applications to open or closed for a team.', inline=False)
    help_embed.add_field(name='!pingteam', value='Admin command to ping all members of your league team.', inline=False)
    help_embed.add_field(name='!pruneteam', value='Admin command to remove players from your team that are no longer in this server.', inline=False)
    help_embed.add_field(name='!leagueorder [spot 1] [spot 2]', value='Admin command to swap the positions of two players in the teams info page.', inline=False)

    await message.channel.send(embed=help_embed)
