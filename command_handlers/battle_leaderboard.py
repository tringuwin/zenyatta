
async def battle_leaderboard_handler(db, message):

    users = db['users']
    all_users = users.find()

    sort_users = []

    for user in all_users:
        if 'wlt' in user:

            uwlt = user['wlt']
            if uwlt['w'] + uwlt['l'] + uwlt['t'] > 0:
                new_obj = {
                    'battle_tag': user['battle_tag'].split('#')[0],
                    'w': uwlt['w'],
                    'l': uwlt['l'],
                    't': uwlt['t'],
                    'percent': round((float(uwlt['w']) /  float( uwlt['w'] + uwlt['l'] )) * 100, 2),
                    'points': uwlt['w'] - uwlt['l']
                }
                sort_users.append(new_obj)

    final_users = sorted(sort_users, key=lambda x: (-x['percent'], -x['points']))

    final_string = '**XP BATTLE LEADERBOARD**'

    for x in range(10):
        print(x)
        rank_user = final_users[x]
        final_string += '\n'+str(x)+'. **'+rank_user['battle_tag']+'** | %'+str(rank_user['percent'])+' | W: '+str(rank_user['w'])+' | L: '+str(rank_user['l'])+' | T: '+str(rank_user['t'])

    final_string += '\n------------------------'
    final_string += '\nSee the full token leaderboard here!\nhttps://spicyragu.netlify.app/battle-leaderboard'

    await message.channel.send(final_string)

    

