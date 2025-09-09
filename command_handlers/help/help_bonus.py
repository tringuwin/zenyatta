
import discord

from safe_send import safe_add_field, safe_create_embed, safe_send_embed

async def help_bonus_handler(message):
    
    help_embed = safe_create_embed('List of bonus commands:')

    safe_add_field(help_embed, '!donate [@user] [number of tokens]', 'Donate tokens to another user in this server!', False)
    safe_add_field(help_embed, '!sellpickaxe', 'Sell 1 Pickaxe for 15 tokens', False)
    safe_add_field(help_embed, '!invitedby [@user]', 'Mention the user that invited you for you both to get the invite reward.', False)
    safe_add_field(help_embed, '!leaguexp', 'Shows the XP Leaderboard for the monthly XP challenge.', False)
    safe_add_field(help_embed, '!leaguexptotal', 'Shows the XP Leaderboard for the total XP teams have earned (since Season 3).', False)
    safe_add_field(help_embed, '!store', 'Get a link to the official SOL Merch Store.', False)
    safe_add_field(help_embed, '!auctiontimer', 'Shows how much time is left until the Daily Auction ends.', False)
    safe_add_field(help_embed, '!leaderboard', 'Shows the Top 10 players by Level/XP and links to the full server leaderboard.', False)
    safe_add_field(help_embed, '!tokenleaderboard', 'See the top 10 users with the most tokens in the server.', False)
    safe_add_field(help_embed, '!hello', 'Say hi to the Scovi bot', False)
    safe_add_field(help_embed, '!gg ez', 'Scovi will respond with one of the classic "gg ez" responses.', False)
    safe_add_field(help_embed, '!whichhero [question]', 'Ask the Scovi bot a question and it will respond with a hero. (Example: !whichhero should be nerfed?)', False)
    safe_add_field(help_embed, '!bandforband @user', 'Challenge another user to see who has the higher net worth!', False)

    await safe_send_embed(message.channel, help_embed)
