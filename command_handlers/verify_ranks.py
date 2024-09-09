
from common_messages import not_registered_response
from user import get_user_ranks, user_exists
import requests
from bs4 import BeautifulSoup

tiers_and_value = {
    'Rank_Bronze': 100,
    'Rank_Silver': 200,
    'Rank_Gold': 300,
    'Rank_Platinum': 400,
    'Rank_Diamond': 500,
    'Rank_Master': 600,
    'Rank_GrandMaster': 700,
    'Rank_Champ': 800,
}

divs_and_value = {
    'Division_5': 1,
    'Division_4': 2,
    'Division_3': 3,
    'Division_2': 2,
    'Division_1': 1
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
    response = requests.get(web_page)
    #response = requests.get('https://overwatch.blizzard.com/en-us/career/DVa-13431/')
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
        rank_parts = pc_child_div.find_all('img', class_='Profile-playerSummary--rank')
        rank_tier = rank_parts[0]
        tier_text = rank_tier['src']
        rank_div = rank_parts[1]
        div_text = rank_div['src']
 
        print('-----------')
        print('tier_text')
        print(tier_text)
        print('div_text')
        print(div_text)

        roles_and_ranks.append({
            'role': role_text,
            'tier': tier_text,
            'div': div_text
        })
        print('pc')
        print('---')
        print('role: '+role_text)
        print('tier: '+tier_text)
        print('div: '+div_text)

    cs_target_div = soup.find('div', class_='controller-view')
    cs_child_divs = cs_target_div.find_all('div', recursive=False)

    for cs_child_div in cs_child_divs:
        role_holder = cs_child_div.find('div', class_='Profile-playerSummary--role')
        role = role_holder.find('img')
        role_text = role['src']
        rank_parts = cs_child_div.find_all('img', class_='Profile-playerSummary--rank')
        rank_tier = rank_parts[0]
        tier_text = rank_tier['src']
        rank_div = rank_parts[1]
        div_text = rank_div['src']
 
        print('-----------')
        print('tier_text')
        print(tier_text)
        print('div_text')
        print(div_text)

        roles_and_ranks.append({
            'role': role_text,
            'tier': tier_text,
            'div': div_text
        })
        print('cs')
        print('---')
        print('role: '+role_text)
        print('tier: '+tier_text)
        print('div: '+div_text)

    player_roles = {
        'tank': ['none', 0],
        'offense': ['none',  0],
        'support': ['none',  0]
    }

    for group in roles_and_ranks:

        this_role = 'none'
        role_text = group['role']
        print('doing group')
        print(group)

        if role_text.find('open') != -1:
            print('skipping open')
            continue

        for example_role in role_list:
            if role_text.find(example_role) != -1:
                this_role = example_role
                break

        if this_role == 'none':
            raise Exception('Could not find role for role string: '+role_text)
        

        tier_text = group['tier'].lower()
        tier = 'none'
        tier_value = 0
        for tier_name in tiers_and_value:
            if tier_text.find(tier_name.lower()) != -1:
                tier = tier_name
                tier_value = tiers_and_value[tier_name]
                break

        if tier == 'none':
            raise Exception('Could not find tier for tier string: '+tier_text)
        

        div_text = group['div'].lower()
        div = 'none'
        div_value = 0
        for div_name in divs_and_value:
            if div_text.find(div_name.lower()) != -1:
                div = div_name
                div_value = divs_and_value[div_name]
                break

        if div == 'none':
            raise Exception('Could not find div for div string: '+div_text)

        rank_value = tier_value + div_value
        rank = tier+' '+div
        
        if player_roles[this_role][1] == 0:
            player_roles[this_role] = [rank, rank_value, tier, div]
        else:
            if player_roles[this_role][1] < rank_value:
                 player_roles[this_role] = [rank, rank_value, tier, div]

    user_ranks = get_user_ranks(user)
    print('before ranks')
    print(user_ranks)

    for role_id in role_list:
        if role_id in player_roles:
            role_info = player_roles[role_id]
            user_ranks[role_id] = {
                'tier': role_info[2],
                'div': role_info[3]
            }
        else:
            user_ranks[role_id] = {
                'tier': 'none',
                'div': 'none'
            }

    print('after ranks')
    print(user_ranks)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"ranks": user_ranks}})
    await message.channel.send('Ranks updated successfully!')

        

        







    


