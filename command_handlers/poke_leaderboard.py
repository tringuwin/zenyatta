
from poke_data import ALL_POKE_NUM


async def poke_leaderboard_handler(db, message):
    
    users = db['users']
    all_users = users.find()

    filtered_users = [user for user in all_users if 'pokedex' in user]

    sorted_users = sorted(filtered_users, key=lambda x: x["pokedex"], reverse=True)

    top_10_users = sorted_users[:10]

    final_string = '<:poke:1233203367636107345> **SERVER POKEDEX LEADERBOARD:** <:poke:1233203367636107345>\n'
    user_index = 1
    for user in top_10_users:

        user_tag = user['battle_tag']
        first_part = user_tag.split('#')[0]

        final_string += "**"+str(user_index)+".** "+first_part
        final_string += ' | '+str(user['tokens'])+'/'+str(ALL_POKE_NUM)+'\n'
        user_index += 1

    # final_string += '------------------------\n'
    # final_string += 'See the full token leaderboard here!\nhttps://spicyragu.netlify.app/token-leaderboard'

    await message.channel.send(final_string)