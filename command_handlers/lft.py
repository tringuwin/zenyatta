
def get_lft_user(db, member, user):

    lft_users = db['lft_users']
    lft_user = lft_users.find_one({'user_id': member.id})
    if lft_user:
        return False, lft_user
    
    avatar = member.display_avatar
    avatar_link = ''
    if avatar:
        avatar_link = avatar.url

    disc = member.discriminator
    final_name = member.name
    if disc != '0':
        final_name = final_name+"#"+disc

    return True, {
        
        'user_id': member.id,
        'is_on': True,
        'image_link': avatar_link,
        'battle_tag': user['battle_tag'],
        'discord_username': final_name,
        'roles': [],
        'heroes': {
            'hero1': 'None',
            'hero2': 'None',
            'hero3': 'None',
            'hero4': 'None'
        }
    }

