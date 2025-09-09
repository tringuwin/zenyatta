import discord

from safe_send import safe_create_embed, safe_send_embed, safe_add_field

async def help_league_handler(message):

    help_embed = safe_create_embed('List of league commands:')

    safe_add_field(help_embed, '!helpleagueadmin', 'See a list of admin commands for league teams.', False)
    safe_add_field(help_embed, '!schedule', 'See the current league schedule.', False)
    safe_add_field(help_embed, '!teampage [team name]', 'Get a link to a webpage for any league team.', False)
    safe_add_field(help_embed, '!standings', 'See the current league standings.', False)
    safe_add_field(help_embed, '!fanof [team name]', 'Set which league team you are a fan of!', False)
    safe_add_field(help_embed, '!rivalof [team name]', 'Set which league team you are a rival of!', False)
    safe_add_field(help_embed, '!leagueinvites', 'See a list of league teams that you are invited to.', False)
    safe_add_field(help_embed, '!leagueaccept [team name]', 'Accept an invite to join a league team.', False)
    safe_add_field(help_embed, '!leaguedeny [team name]', 'Deny an invite to join a league team.', False)
    safe_add_field(help_embed, '!leagueleave', 'Leave your current league team.', False)
    safe_add_field(help_embed, '!callme Name Here', 'Set how casters should say your name in your matches.', False)

    await safe_send_embed(message.channel, help_embed)