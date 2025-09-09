
import constants
from safe_send import safe_send

async def not_registered_response(message, context='OW'):

    if context == 'OW':

        if message.channel.id == constants.BOT_CHANNEL:
            await safe_send(message.channel, message.author.mention+" It seems like you're not registered yet. Please use this command to register: **!battle YourBattleTagHere#1234**")
        else:
            await safe_send(message.channel, message.author.mention+" It seems like you're not registered yet. Please go to this channel ( https://discord.com/channels/1130553449491210442/1130553489106411591 ) and use this command to register: **!battle YourBattleTagHere#1234**")

    else:

        if message.channel.id == constants.RIVALS_BOT_CHANNEL:
            await safe_send(message.channel, message.author.mention+" It seems like you're not registered yet. Please use this command to register: **!username MarvelRivalsUsername**")
        else:
            await safe_send(message.channel, message.author.mention+" It seems like you're not registered yet. Please go to this channel ( https://discord.com/channels/1130553449491210442/1130553489106411591 ) and use this command to register: **!username MarvelRivalsUsername**")

async def invalid_number_of_params(message):
    await safe_send(message.channel, "Invalid number of parameters. Please check **!help** for more details.")