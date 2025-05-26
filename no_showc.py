import constants
from bracket import no_show

async def no_show_handler(db, message, client):
    word_list = message.content.split()
    if len(word_list) == 2:
        guild = client.get_guild(constants.GUILD_ID)
        await no_show(int(word_list[1]), message, db, guild, client)
    else:
        await message.channel.send("Invalid number of arguments.")