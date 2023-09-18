
from common_messages import not_registered_response
from user import user_exists
import requests
from bs4 import BeautifulSoup



ranks = [
    'BronzeTier-1',
    'BronzeTier-2',
    'BronzeTier-3',
    'BronzeTier-4',
    'BronzeTier-5',
    'SilverTier-1',
    'SilverTier-2',
    'SilverTier-3',
    'SilverTier-4',
    'SilverTier-5',
    'GoldTier-1',
    'GoldTier-2',
    'GoldTier-3',
    'GoldTier-4',
    'GoldTier-5',
    'PlatinumTier-1',
    'PlatinumTier-2',
    'PlatinumTier-3',
    'PlatinumTier-4',
    'PlatinumTier-5',
    'DiamondTier-1',
    
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

    if response:
        print(response)
        content = response.content

        # Step 2: Parse content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Step 3: Find the div by its class name
        target_div = soup.find('div', class_='mouseKeyboard-view')
        child_divs = target_div.find_all('div', recursive=False)
        for child_div in child_divs:
            role_holder = child_div.find('div', class_='Profile-playerSummary--role')
            role = role_holder.find('img')
            role_text = role['src']
            rank = child_div.find('img', class_='Profile-playerSummary--rank')
            rank_text = rank['src']

            print('---')
            print('role: '+role_text)
            print('rank: '+rank_text)


