
from common_messages import not_registered_response
from user import user_exists
import requests
from bs4 import BeautifulSoup


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

        content = response.content

        # Step 2: Parse content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Step 3: Find the div by its class name
        target_div = soup.find('div', class_='mouseKeyboard-view Profile-playerSummary--rankWrapper')
        child_divs = target_div.find_all('div', recursive=False)
        for child_div in child_divs:
            img_class = child_div.find('img')
            print(img_class)
