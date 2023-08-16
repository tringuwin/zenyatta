import discord

async def help_teams_hanlder(message):

    help_embed = discord.Embed(title='List of teams commands:')
    help_embed.add_field(name='!teams', value='See the teams that you are currenrly part of.', inline=False)
    help_embed.add_field(name='!teamdetails [team name]', value='See the details of a specific team.', inline=False)
    help_embed.add_field(name='!maketeam [team size] [team name]', value='Make a new team.', inline=False)
    help_embed.add_field(name='!invite [@player] [team name]', value='Invite a user to a team you own by mentioning them.', inline=False)
    help_embed.add_field(name='!myinvites', value='See a list of teams you are invited to.', inline=False)
    help_embed.add_field(name='!acceptinvite [team name]', value='Accept an invite to a team.', inline=False)
    help_embed.add_field(name='!denyinvite [team name]', value='Deny an invite to a team.', inline=False)
    help_embed.add_field(name='!leaveteam [team name]', value='Leave a team.', inline=False)
    help_embed.add_field(name='!deleteteam [team name]', value='Delete a team you own.', inline=False)

    await message.channel.send(embed=help_embed)