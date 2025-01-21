
import constants
from discord_actions import get_guild


async def message_about_drop(client, user, reward_info):

    guild = await get_guild(client)
    redemptions_channel = guild.get_channel(constants.OFFER_REDEMPTIONS_CHANNEL_ID)

    user_mention = '<@'+str(user['discord_id'])+'>'

    await redemptions_channel.send(user_mention+' just got the reward: '+reward_info['user_message'])