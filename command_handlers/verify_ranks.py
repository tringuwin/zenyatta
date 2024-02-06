
from common_messages import not_registered_response
from user import user_exists
import requests
from bs4 import BeautifulSoup

ranks_and_value = {
    'BronzeTier-5': 1,
    'BronzeTier-4': 2,
    'BronzeTier-3': 3,
    'BronzeTier-2': 4,
    'BronzeTier-1': 5,
    'SilverTier-5': 6,
    'SilverTier-4': 7,
    'SilverTier-3': 8,
    'SilverTier-2': 9,
    'SilverTier-1': 10,
    'GoldTier-5': 11,
    'GoldTier-4': 12,
    'GoldTier-3': 13,
    'GoldTier-2': 14,
    'GoldTier-1': 15,
    'PlatinumTier-5': 16,
    'PlatinumTier-4': 17,
    'PlatinumTier-3': 18,
    'PlatinumTier-2': 19,
    'PlatinumTier-1': 20,
    'DiamondTier-5': 21,
    'DiamondTier-4': 22,
    'DiamondTier-3': 23,
    'DiamondTier-2': 24,
    'DiamondTier-1': 25,
    'MasterTier-5': 26,
    'MasterTier-4': 27,
    'MasterTier-3': 28,
    'MasterTier-2': 29,
    'MasterTier-1': 30,
    'GrandMasterTier-5': 31,
    'GrandMasterTier-4': 32,
    'GrandMasterTier-3': 33,
    'GrandMasterTier-2': 34,
    'GrandMasterTier-1': 35,
}

role_list = [
    'tank',
    'offense',
    'support'
]

async def verify_ranks_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    battle_tag = user['battle_tag']
    web_page = 'https://overwatch.blizzard.com/en-us/career/'
    tag_parts = battle_tag.split('#')
    web_page += tag_parts[0]+'-'+tag_parts[1]
    #response = requests.get(web_page)
    response = requests.get('https://overwatch.blizzard.com/en-us/career/DVa-13431/')
    print('response is:')
    print(response.status_code)

    if response.status_code == 404:
        await message.channel.send("I couldn't find your Overwatch Profile. You may have a private profile, or you may have linked the wrong battle tag. Try **!profile** to see the battle tag you currently have linked.")
        return

    if not response:
        await message.channel.send('Something went wrong! Please try again later.')
        return

    content = response.content

    # Step 2: Parse content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    roles_and_ranks = []

    # Step 3: Find the div by its class name
    pc_target_div = soup.find('div', class_='mouseKeyboard-view')
    pc_child_divs = pc_target_div.find_all('div', recursive=False)

    for pc_child_div in pc_child_divs:
        role_holder = pc_child_div.find('div', class_='Profile-playerSummary--role')
        role = role_holder.find('img')
        role_text = role['src']
        rank = pc_child_div.find('img', class_='Profile-playerSummary--rank')
        rank_text = rank['src']
        roles_and_ranks.append({
            'role': role_text,
            'rank': rank_text
        })
        print('pc')
        print('---')
        print('role: '+role_text)
        print('rank: '+rank_text)

    cs_target_div = soup.find('div', class_='controller-view')
    cs_child_divs = cs_target_div.find_all('div', recursive=False)

    for cs_child_div in cs_child_divs:
        role_holder = cs_child_div.find('svg', class_='Profile-playerSummary--role')
        role = role_holder.find('use')
        role_text = role['xlink:href']
        rank = cs_child_div.find('img', class_='Profile-playerSummary--rank')
        rank_text = rank['src']
        roles_and_ranks.append({
            'role': role_text,
            'rank': rank_text
        })
        print('console')
        print('---')
        print('role: '+role_text)
        print('rank: '+rank_text)

    player_roles = {
        'tank': ['none', 0],
        'offense': ['none', 0],
        'support': ['none', 0]
    }

    for group in roles_and_ranks:

        this_role = 'none'
        role_text = group['role']
        for example_role in role_list:
            if role_text.find(example_role) != -1:
                this_role = example_role
                break

        if this_role == 'none':
            raise Exception('Could not find role for role string: '+role_text)
        
        rank_text = group['rank'].lower()
        rank = 'none'
        rank_value = 0
        for rank_name in ranks_and_value:
            if rank_text.find(rank_name.lower()) != -1:
                rank = rank_name
                rank_value = ranks_and_value[rank_name]
                break

        if rank == 'none':
            raise Exception('Could not find rank for rank string: '+rank_text)
        
        if player_roles[this_role][1] == 0:
            player_roles[this_role] = [rank, rank_value]
        else:
            if player_roles[this_role][1] < rank_value:
                 player_roles[this_role] = [rank, rank_value]

    for final_role_name in player_roles:

        final_value = player_roles[final_role_name]
        if final_value[1] != 0:
            print('FINAL ROLE FOR '+final_role_name+': '+final_value[0])

        

        







    


