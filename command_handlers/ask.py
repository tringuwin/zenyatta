

from open_ai import ask_zen


async def ask_handler(message):

    chopped_command = message.content[5:]
    zen_response = ask_zen(chopped_command)

    await message.reply(zen_response)