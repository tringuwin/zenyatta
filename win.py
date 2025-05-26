import constants
from bracket import won_match

async def win_handler(db, message, client):
    word_list = message.content.split()
    if len(word_list) == 2:
        guild = client.get_guild(constants.GUILD_ID)
        await won_match(int(word_list[1]), message, db, guild, client)
    else:
        await message.channel.send("Invalid number of arguments.")