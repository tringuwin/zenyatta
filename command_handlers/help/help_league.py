import discord

from safe_send import safe_send, safe_send_embed

async def help_league_handler(message):

    help_embed = discord.Embed(title='List of league commands:')
    help_embed.add_field(name='!helpleagueadmin', value='See a list of admin commands for league teams.', inline=False)
    help_embed.add_field(name='!schedule', value='See the current league schedule.', inline=False)
    help_embed.add_field(name='!teampage [team name]', value='Get a link to a webpage for any league team.', inline=False)
    help_embed.add_field(name='!standings', value='See the current league standings.', inline=False)
    help_embed.add_field(name='!fanof [team name]', value='Set which league team you are a fan of!', inline=False)
    help_embed.add_field(name='!rivalof [team name]', value='Set which league team you are a rival of!', inline=False)
    help_embed.add_field(name='!leagueinvites', value='See a list of league teams that you are invited to.', inline=False)
    help_embed.add_field(name='!leagueaccept [team name]', value='Accept an invite to join a league team.', inline=False)
    help_embed.add_field(name='!leaguedeny [team name]', value='Deny an invite to join a league team.', inline=False)
    help_embed.add_field(name='!leagueleave', value='Leave your current league team.', inline=False)
    help_embed.add_field(name='!callme Name Here', value='Set how casters should say your name in your matches.', inline=False)

    await safe_send_embed(message.channel, help_embed)