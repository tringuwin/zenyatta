

from drops.open_spicy_drop.utils.process_drop_reward.utils.message_about_drop import message_about_drop
from drops.open_spicy_drop.utils.process_drop_reward.utils.process_automatic_reward import process_automatic_reward


async def process_drop_reward(db, client, user, reward_info):

    if reward_info['automatic']:
        await process_automatic_reward(db, user, reward_info)

    if reward_info['message_redemptions']:
        await message_about_drop(client, user, reward_info)