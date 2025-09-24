
import discord

from safe_send import safe_add_field, safe_create_embed, safe_send, safe_send_embed

async def help_league_admin_handler(message):

    help_embed = safe_create_embed('List of league team admin commands:')

    safe_add_field(help_embed, '!helpally', 'Show a list of league team admin commands related to League Team Allies and Rivals.', False)
    safe_add_field(help_embed, '!setlineup', 'The bot will DM you a secure link to the SOL website to set the lineup for your team.', False)
    safe_add_field(help_embed, '!invite @User', 'Admin command to invite a user to your league team', False)
    safe_add_field(help_embed, '!leaguecancelinvite @User', "Admin command to cancel a user's pending invite to your team.", False)
    safe_add_field(help_embed, '!changetpp username [tpp number]', 'Admin command to change the TPP of a player on your league team.', False)
    safe_add_field(help_embed, '!changerole @Player [role info]', 'Admin command to change the role of a player on your league team.', False)
    safe_add_field(help_embed, '!maketeamadmin @Player', 'Owner command to make a member of your league team an admin.', False)
    safe_add_field(help_embed, '!removeteamadmin @Player', 'Owner command to remove admin role from a member of your league team.', False)
    safe_add_field(help_embed, '!leaguekick @Player', 'Admin command to kick a player from your league team.', False)
    safe_add_field(help_embed, '!pingteam', 'Admin command to ping all members of your league team.', False)
    safe_add_field(help_embed, '!pruneteam', 'Admin command to remove players from your team that are no longer in this server.', False)
    safe_add_field(help_embed, '!leagueorder [spot 1] [spot 2]', 'Admin command to swap the positions of two players in the teams info page.', False)

    await safe_send_embed(message.channel, help_embed)