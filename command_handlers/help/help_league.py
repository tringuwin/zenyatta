import discord

async def help_league_handler(message):

    help_embed = discord.Embed(title='List of commands:')
    help_embed.add_field(name='!leagueinvite @User', value='Admin command to invite a user to your league team', inline=False)
    help_embed.add_field(name='!leaguecancelinvite @User', value="Admin command to cancel a user's pending invite to your team.", inline=False)
    help_embed.add_field(name='!leagueinvites', value='See a list of league teams that you are invited to.', inline=False)
    help_embed.add_field(name='!leagueaccept [team name]', value='Accept an invite to join a league team. Please make sure to use exact team name and capitilization.', inline=False)
    help_embed.add_field(name='!changetpp @Player [tpp number]', value='Admin command to change the TPP of a player on your league team.', inline=False)
    help_embed.add_field(name='!changerole @Player [role info]', value='Admin command to change the role of a player on your league team.', inline=False)
    help_embed.add_field(name='!maketeamadmin @Player', value='Owner command to make a member of your league team an admin.', inline=False)
    help_embed.add_field(name='!removeteamadmin @Player', value='Owner command to remove admin role from a member of your league team.', inline=False)
    help_embed.add_field(name='!leagueleave', value='Leave your current league team.', inline=False)
    help_embed.add_field(name='!leaguekick', value='Admin command to kick a player from your league team.', inline=False)

    await message.channel.send(embed=help_embed)